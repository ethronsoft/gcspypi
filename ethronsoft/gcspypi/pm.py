import datetime
import re
import pip
from google.cloud import storage

from pb import *
from utils import *


class PackageManager(object):
    def __init__(self, repo_name, overwrite=False, mirroring=True, install_deps=True):
        self.__bucket_name = repo_name
        self.__overwrite = overwrite
        self.__mirroring = mirroring
        self.__install_deps = install_deps
        self.__prog = re.compile("((?:\w|-)*)(==|=?<|=?>)?((?:\d*\.?){0,3})?,?(==|=?<|=?>)?((?:\d*\.?){0,3})?")
        self.__repo_cache = []
        self.refresh_cache()

    def upload(self, pkg, filename):
        if not pkg.version:
            raise Exception("Version must be specified when uploading a package")
        current = self.search(pkg.name + "==" + pkg.version)
        if current and current.type == pkg.type and not self.__overwrite:
            raise Exception("upload would result in overwrite but overwrite mode is not enabled")
        blob = self.__get_bucket().blob(pkg.name + "/" + pkg.version + "/" + os.path.split(filename)[1])
        blob.upload_from_filename(filename)

    def download_by_name(self, obj_name, dest):
        to_install = ""
        for path in self.__repo_cache:
            if obj_name in path:
                to_install = path
                break
        if to_install:
            output = os.path.join(dest, os.path.split(to_install)[1])
            blob = self.__get_bucket().blob(to_install)
            blob.download_to_filename(output)
            return output
        else:
            return ""

    def download(self, pkg, dest, preferred_type):
        if not pkg.version:
            pkg = self.search(pkg.name)
            if not pkg: return ""
        target = pkg.full_name.replace(":", "/")
        l = [item for item in self.__repo_cache if target in item]
        if l:
            to_install = l[0]
            for p in l:
                if utils.get_package_type(p) == preferred_type:
                    to_install = p
                    break
            #download first
            blob = self.__get_bucket().blob(to_install)
            output = os.path.join(dest, os.path.split(to_install)[1])
            blob.download_to_filename(output)
            return output
        else:
            return ""

    def list_items(self, prefix="", from_cache=False):
        if from_cache:
            return [item for item in self.__repo_cache if prefix in item]
        else:
            return sorted(map(lambda b: b.name, self.__get_bucket().list_blobs(prefix=prefix)))

    def search(self, syntax):
        packages = items_to_package(self.__repo_cache)
        #search the repo for packages matching the syntax
        match = self.__prog.match(syntax)
        count = len(match.groups())
        name = match.group(1) if count > 0 else ""
        firstop = match.group(2) if count > 1 else ""
        firstv  = match.group(3) if count > 2 else ""
        secondop = match.group(4) if count > 3 else ""
        secondv  = match.group(5) if count > 4 else ""
        if not name:
            raise Exception("missing package name")
        if (not firstop and firstv) or (not secondop and secondv):
            raise Exception("cannot specify a version number without an operator")
        return pkg_range_query(packages, name.replace("_", "-"), firstop, firstv, secondop, secondv)

    def remove(self, pkg):
        bucket = self.__get_bucket()
        l = self.list_items(prefix=pkg.name + "/" + pkg.version, from_cache=True)
        for x in l:
            try:
                bucket.blob(x).delete()
                return True
            except Exception:
                return False

    def install(self, syntax, preferred_type):
        pkg = self.search(syntax)
        is_internal = pkg is not None
        if not is_internal:
            if self.__mirroring:
                self.__pip_install(syntax)
            else:
                print "{0} not in {1} repository".format(pkg.full_nam, self.__bucket_name)
        else:
            try:
                tmp = tempfile.mkdtemp()
                root_pkg = self.download(pkg, tmp, preferred_type)
                if not root_pkg:
                    return
                if self.__install_deps:
                    # let's separate all the internal requirements from the public ones.
                    # let's install the internal requirements ourselves and delegate the public ones to pip install.
                    # Then, once the requirements are installed, let's call pip install on the package itself

                    # packages to scan for requirements
                    scan_targets = set([root_pkg])
                    # names of internal requirements
                    internal_reqs = set([])
                    # names of public requirements
                    public_reqs = set([])
                    while scan_targets:
                        scanned_pkg = PackageBuilder(scan_targets.pop()).build()
                        new_internal_reqs = self.__find_internal_requirements(scanned_pkg)
                        internal_reqs.union(new_internal_reqs)
                        public_reqs = public_reqs.union(scanned_pkg.requirements - new_internal_reqs)
                        # Let's scan the new internal requirements as they may
                        # themselves point to more internal and public requirements.
                        for inreq in new_internal_reqs:
                            req_pkg = self.search(inreq)
                            req_pkg_installed = self.download(req_pkg, tmp, preferred_type)
                            if req_pkg_installed:
                                scan_targets.add(req_pkg_installed)

                    #let's proceed installing all public requirements first
                    self.__public_install(public_reqs)
                    #let's continue with our private requirements
                    self.__internal_install(internal_reqs, tmp)
                    #then let's use pip install to install the orignal package.
                    #because we have already taken care of dependendencies, we can
                    #use pip --no-dependencies flag
                    self.__pip_install(root_pkg, ["--no-dependencies"])
                else:
                    self.__pip_install(root_pkg, ["--no-dependencies"])
            finally:
                shutil.rmtree(tmp, ignore_errors=True)

    def uninstall(self, pkg):
        pip.main(["uninstall", pkg.full_name.replace(":", "==")])

    def clone(self, root):
        cwd = os.getcwd()
        try:
            tmp = os.path.join(root,"__tmp")
            os.makedirs(tmp)
            for path in self.__repo_cache:
                dest = os.path.join(tmp, path)
                os.makedirs(os.path.split(dest)[0])
                blob = self.__get_bucket().blob(path)
                blob.download_to_filename(dest)
            millis = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
            zip_name = os.path.join(root, "{}_{}.zip".format(self.__bucket_name, millis))
            with zipfile.ZipFile(zip_name, "w") as z:
                os.chdir(tmp)
                for r, ds, fs in os.walk("."):
                    for f in fs:
                        z.write(os.path.join(r, f))
            print "Successfully cloned repository {} to {}".format(self.__bucket_name, zip_name)
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmp)


    def restore(self, zip_repo):
        if self.__repo_cache:
            x = raw_input("Repository {} is not empty.\nDo you want to attempt to push into an existing repository? [y|n]: "
                      .format(self.__bucket_name))
            if x.strip() == "y":
                self.__overwrite = True
            else:
                print "Aborting operation"
                return
        tmp = tempfile.mkdtemp()
        with zipfile.ZipFile(zip_repo, "r") as z:
            z.extractall(tmp)
        for r, ds, fs in os.walk(tmp):
            for f in fs:
                pkg = PackageBuilder(os.path.join(r, f)).build()
                self.upload(pkg, os.path.join(r, f))

    def refresh_cache(self):
        self.__repo_cache = self.list_items()

    def __get_bucket(self):
        ##return a client using the current default login
        ##set with: gcloud auth application-default login
        return storage.Client().bucket(self.__bucket_name)

    def __find_internal_requirements(self, pkg):
        res =  set([])
        for req in pkg.requirements:
            if self.search(req):
                res.add(req)
        return res

    def __internal_install(self, requirements, install_dir):
        #install the private package using pip.
        #Because all dependendencies (public or internal)
        #that one of these packages may have is already either
        #in this requriments list or in the one passed to
        #public_install,we can use pip --no-dependencies flag
        for r in requirements:
            #we have saved the temp packages using Package::full_name().replace(":,"_")
            #so let's get back our package to reference that file
            pkg = Package.from_text(r)
            self.__pip_install(os.path.join(install_dir,pkg.full_name.replace(":", "_")), ["--no-dependencies"])

    def __public_install(self, requirements):
        for r in requirements:
            self.__pip_install(r)

    def __pip_install(self, resource, flags=[]):
        pip.main(["install", resource] + flags)


