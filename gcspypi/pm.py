from google.cloud import storage
from pb import *
import pip
import re
from utils import *

class PackageManager(object):
    def __init__(self, repo_name, overwrite=False, mirroring=True, install_deps=True):
        self.__bucket_name = repo_name
        self.__overwrite = overwrite
        self.__mirroring = mirroring
        self.__install_deps = install_deps
        self.__prog = re.compile("(\w*)(==|=?<|=?>)?((?:\d*\.?){0,3})?,?(==|=?<|=?>)?((?:\d*\.?){0,3})?")
        self.__repo_cache = []

    def upload(self, pkg, filename):
        if not pkg.version:
            raise Exception("Version must be specified when uploading a package")
        current = self.search(pkg.name + "==" + pkg.version)
        if current and not self.__overwrite:
            raise Exception("upload would result in overwrite but overwrite mode is not enabled")
        blob = self.__get_bucket().blob(pkg.name + "/" + pkg.version + "/" + os.path.split(filename)[1])
        blob.upload_from_filename(filename)

    def download(self, pkg, dest):
        if not pkg.version:
            last = self.search(pkg.name)
            lastv = last.version if last else "0.0.0"
            newv  = lastv.version[:-2] + str(int(lastv.version[-1]))
            repo_object_name = pkg.name + "/" + newv
        else:
            repo_object_name = pkg.name + "/" + pkg.version
        #get the first available file under this name and version
        l = self.__get_bucket.list_blobs(prefix=pkg.name + "/" + pkg.version)
        if l:
            blob = self.__get_bucket.blob(l[0])
            output = os.path.join(dest,os.path.split(l.name[0])[1])
            blob.download_to_file(output)
            return output
        else:
            return ""

    def list(self, prefix=""):
        print "listing"
        res = []
        l = self.__get_bucket.list_blobs(prefix=prefix)
        for x in l:
            tokens = x.name.split("/")
            res = Package(tokens[-3], tokens[-2])
        # let's return ordered, for searching and visual reasons
        return sorted(res, cmp=pkg_comp_name_version)

    def search(self, syntax):
        if not self.__repo_cache:
            self.__repo_cache = list()
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
        return pkg_range_query(self.__repo_cache, name, firstop, firstv, secondop, secondv)

    def remove(self, pkg):
        bucket = self.__get_bucket()
        l = bucket.list_blobs(prefix=pkg.name + "/" + pkg.version)
        for x in l:
            bucket.blob(x.name).delete()

    def install(self, syntax):
        print "installing"
        if not self.__repo_cache:
            self.__repo_cache = list()
        for token in syntax.split():
            pkg = self.search(token)
            is_internal = pkg is not None
            if not is_internal:
                if self.__mirroring:
                    print "mirrored pip install {}".format(pkg.full_name)
                    self.__pip_install(pkg.full_name)
                else:
                    print "{0} not in {1} repository".format(pkg.full_nam,self.__bucket_name)
            else:
                try:
                    tmp = tempfile.mkdtemp()
                    root_pkg_install = os.path.join(tmp,pkg.full_name.replace(":", "_"))
                    self.download(pkg, root_pkg_install)

                    if self.__install_deps:
                        #let's separate all the internal requirements from the public ones.
                        #let's install the internal requirements ourselves and delegate the public ones to pip install.
                        #Then, once the requirements are installed, let's call pip install on the package itself

                        #packages to scan for requirements
                        scan_targets = set([root_pkg_install])
                        #names of internal requirements
                        internal_reqs = set([])
                        #names of public requirements
                        public_reqs = set([])
                        while scan_targets:
                            scanned_pkg = PackageBuilder(scan_targets.pop()).build()
                            new_internal_reqs = self.__find_internal_requirements(scanned_pkg)
                            internal_reqs.union(new_internal_reqs)
                            public_reqs.union(scanned_pkg.requirements - new_internal_reqs)
                            #Let's scan the new internal requirements as they may
                            #themselves point to more internal and public requirements.
                            for inreq in new_internal_reqs:
                                req_pkg = Package.from_text(inreq)
                                req_pkg_install = os.path.join(tmp,req_pkg.full_name.replace(":", "_"))
                                self.download(req_pkg,req_pkg_install)
                                scan_targets.add(req_pkg_install)

                        #let's proceed installing all public requirements first
                        self.__public_install(public_reqs)
                        #let's continue with our private requirements
                        self.__internal_install(internal_reqs)
                        #then let's use pip install to install the orignal package.
                        #because we have already taken care of dependendencies, we can
                        #use pip --no-dependencies flag
                        self.__pip_install(root_pkg_install, ["--no-dependencies"])
                    else:
                        self.__pip_install(root_pkg_install, ["--no-dependencies"])
                finally:
                    shutil.rmtree(tmp, ignore_errors=True)


    def uninistall(self, pkg):
        pip.main(["uninstall", pkg.full_name.replace(":", "==")])

    def clear_cache(self):
        self.__repo_cache = []

    def __get_bucket(self):
        ##return a client using the current default login
        ##set with: gcloud auth application-default login
        return storage.Client().bucket(self.__bucket_name)

    def __find_internal_requirements(self,pkg):
        return set([])

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


