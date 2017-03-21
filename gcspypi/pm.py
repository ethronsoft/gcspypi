from google.cloud import storage
from pb import *


class PackageManager(object):
    def __init__(self, repo_name, overwrite=False, mirroring=True, install_deps=True):
        self.__bucket_name = repo_name
        self.__overwrite = overwrite
        self.__mirroring = mirroring
        self.__install_deps = install_deps
        self.__repo_cache = []

    def upload(self, pkg, overwrite):
        print "uploading"

        # repo_object_name = "some"
        # blob = self.__get_bucket.blob(repo_object_name)
        # blob.upload_from_filename(filename)

    def download(self, pkg, dest):
        print "downloading"
        return False
        # target_file_name = "some.in"
        # output_file_name = "some.out"
        # blob = self.__get_bucket.blob(repo_object_name)
        # blob.download_to_filename(output_file_name)

    def list(self, prefix=""):
        print "listing"
        # list_res = self.__get_bucket.list_blobs(prefix=prefix)
        ## let's return ordered, for searching and visual reasons
        # def comp(i, x):
        #	if   (i.name == x.name): return 0
        #	elif (i.name <  x.name): return -1
        #	else				      : return 1
        # return sorted(list_res,cmp=comp)

    def search(self, pkgs):
        #remove all pkgs that are not in the repo
        return pkgs

    def remove(self, pkg):
        print "removing"

    def install(self, pkg):
        print "installing"
        if not self.__repo_cache:
            self.__repo_cache = list()

        is_internal = False#TODO
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
                            req_pkg = PackageParser(inreq).parse()
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
        print "uninstalling"

    def clear_cache(self):
        self.__repo_cache = []


    def __get_bucket(self):
        ###return a client using the current default login
        ###set with: gcloud auth application-default login
        # return storage.Client().bucket(self.__bucket_name)
        pass

    def __find_internal_requirements(self,pkg):
        return set([])

    def __internal_install(self, requirements, install_dir):
        #install the private package using pip.
        #Because all dependendencies (public or internal)
        #that one of these packages may have is already either
        #in this requriments list or in the one passed to
        #__public_install,we can use pip --no-dependencies flag
        for r in requirements:
            #we have saved the temp packages using Package::full_name().replace(":,"_")
            #so let's get back our package to reference that file
            pkg = PackageParser(r).parse()
            self.__pip_install(os.path.join(install_dir,pkg.full_name.replace(":", "_")), ["--no-dependencies"])


    def __public_install(self, requirements):
        for r in requirements:
            self.__pip_install(r)

    def __pip_install(self, resource, flags=[]):

        pass
