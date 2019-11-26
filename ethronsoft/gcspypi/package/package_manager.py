from __future__ import print_function
from ethronsoft.gcspypi.exceptions import InvalidParameter, InvalidState
from ethronsoft.gcspypi.package.package_builder import Package, PackageBuilder
from ethronsoft.gcspypi.utilities.queries import get_package_type, items_to_package, pkg_range_query
from ethronsoft.gcspypi.utilities.console import Console

import os
import sys
import datetime
import re
import subprocess
import tempfile
import shutil
import zipfile
from glob import glob



class PackageInstaller(object): # pragma: no cover

    def __init__(self, is_python3):
        self.__is_python3 = is_python3

    def install(self, resource, flags=[]):
        if self.__is_python3:
            subprocess.check_call(["python3", "-m", "pip","install", resource] + flags)
        else:
            subprocess.check_call(["python", "-m", "pip","install", resource] + flags)

    def uninstall(self, pkg):
        if self.__is_python3:
            subprocess.check_call(["python3", "-m", "pip","uninstall", pkg.full_name.replace(":", "==")])
        else:
            subprocess.check_call(["python", "-m", "pip","uninstall", pkg.full_name.replace(":", "==")])

class PackageManager(object):

    def __init__(self, repo, console, installer=None, is_python3=False, overwrite=False, mirroring=True, install_deps=True):
        self.__repo = repo
        self.__console = console
        self.__overwrite = overwrite
        self.__mirroring = mirroring
        if installer:
            self.__installer = installer
        else:
            self.__installer = PackageInstaller(is_python3 = is_python3)
        self.__install_deps = install_deps
        self.__is_python3 = is_python3
        self.__prog = re.compile("((?:\w|-)*)(==|<=?|>=?)?((?:\d*\.?){0,3})?,?(==|<=?|>=?)?((?:\d*\.?){0,3})?")
        self.__repo_cache = []
        self.refresh_cache()

    def upload(self, pkg, filename):
        if not pkg.version:
            raise InvalidParameter("Version must be specified when uploading a package")
        current = self.search(pkg.name + "==" + pkg.version)
        if current and current.type == pkg.type and not self.__overwrite:
            raise InvalidState("upload would result in overwrite but overwrite mode is not enabled")
        with open(filename, "rb") as f:
            self.__repo.upload_file(Package.repo_name(pkg, filename), f)
        self.refresh_cache()

    def download_by_name(self, obj_name, dest):
        to_install = ""
        for path in self.__repo_cache:
            if obj_name in path:
                to_install = path
                break
        if to_install:
            output = os.path.join(dest, os.path.split(to_install)[1])
            with open(output, "wb") as f:
                self.__repo.download_file(to_install, f)
            return output
        else:
            return ""

    def download(self, pkg, dest, preferred_type):
        if not pkg.version:
            pkg = self.search(pkg.name)
            if not pkg: return ""
        target = pkg.full_name.replace(":", "/")
        matches = [item for item in self.__repo_cache if target in item]
        if matches:
            #we get the first one unless we find a preferred match
            to_install = matches[0]
            for p in matches:
                if get_package_type(p) == preferred_type:
                    to_install = p
                    break
            #download
            output = os.path.join(dest, os.path.split(to_install)[1])
            with open(output, "wb") as f:
                self.__repo.download_file(to_install, f)
            return output
        else:
            return ""

    def list_items(self, prefix="", from_cache=False):
        if from_cache:
            return [item for item in self.__repo_cache if prefix in item]
        else:
            return sorted(self.__repo.list(prefix=prefix))

    def search(self, syntax):
        packages = items_to_package(self.__repo_cache, unique=True)
        #search the repo for packages matching the syntax
        match = self.__prog.match(syntax)
        count = len(match.groups())
        name = match.group(1) if count > 0 else ""
        firstop = match.group(2) if count > 1 else ""
        firstv  = match.group(3) if count > 2 else ""
        secondop = match.group(4) if count > 3 else ""
        secondv  = match.group(5) if count > 4 else ""
        if not name:
            raise InvalidParameter("missing package name")
        if (not firstop and firstv) or (not secondop and secondv):
            raise InvalidParameter("cannot specify a version number without an operator")
        return pkg_range_query(packages, name.replace("_", "-"), firstop, firstv, secondop, secondv)

    def remove(self, pkg, interactive=True):
        matches = self.list_items(prefix=pkg.name + "/" + pkg.version, from_cache=True)
        if not matches:
            return False
        self.__console.info("The following packages will be removed: ")
        self.__console.info("\n".join(matches))
        if interactive: # pragma: no cover
            ok = self.__console.selection("Do you want to proceed?", ["y", "n"])
            if ok.upper().strip() != "Y":
                self.__console.warning("Aborting deletion of {}".format(pkg.name))
                return False
        for x in matches:
            try:
                self.__repo.delete(x)
            except Exception:
                self.__console.error("Error while removing {}".format(x))
                return False
        self.refresh_cache()
        # self.__repo_cache = [x for x in self.__repo_cache if not "{}/".format(pkg.name) in x]
        return True

    def install(self, syntax, preferred_type, no_user):
        pkg = self.search(syntax)
        is_internal = pkg is not None
        if not is_internal:
            if self.__mirroring:
                self.__installer.install(syntax)
            else:
                self.__console.warning("{0} not in repository".format(syntax))
        else:
            try:
                tmp = tempfile.mkdtemp()
                root_dir = os.path.join(tmp, pkg.full_name.replace(":", "_"))
                os.mkdir(root_dir)
                root_pkg = self.download(pkg, root_dir, preferred_type)
                #Note: if we got here is because pkg was found in the repository
                #so the condition below should be redundant
                # if not root_pkg:
                    # return False
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
                        public_reqs = public_reqs.union(scanned_pkg.requirements - new_internal_reqs)
                        # Let's scan the new internal requirements as they may
                        # themselves point to more internal and public requirements.
                        for inreq in new_internal_reqs:
                            req_pkg = self.search(inreq)
                            req_dir = os.path.join(tmp, req_pkg.full_name.replace(":", "_"))
                            os.mkdir(req_dir)
                            req_pkg_installed = self.download(req_pkg, req_dir, preferred_type)
                            if req_pkg_installed:
                                internal_reqs.add(req_pkg.full_name.replace(":", "=="))
                                scan_targets.add(req_pkg_installed)

                    #let's proceed installing all public requirements first
                    pub_flags = []
                    if not no_user: pub_flags.append("--user")
                    self.__public_install(public_reqs, pub_flags)
                    #let's continue with our private requirements
                    #Because all dependendencies (public or internal)
                    #that one of these packages may have is already either
                    #in this requriments list or in the one passed to
                    #public_install,we can use pip --no-dependencies flag
                    intern_flags = ["--no-dependencies"]
                    if not no_user: intern_flags.append("--user")
                    self.__internal_install(internal_reqs, tmp, intern_flags)
                    #then let's use pip install to install the original package.
                    #because we have already taken care of dependendencies, we can
                    #use pip --no-dependencies flag
                    root_flags = ["--no-dependencies"]
                    if not no_user: root_flags.append("--user")
                    self.__installer.install(root_pkg, root_flags)
                else:
                    root_flags = ["--no-dependencies", "--user"]
                    if not no_user: root_flags.append("--user")
                    self.__installer.install(root_pkg, root_flags)
            finally:
                shutil.rmtree(tmp, ignore_errors=True)

    def uninstall(self, pkg):
        self.__installer.uninstall(pkg)
        # subprocess.check_call(["python", "-m", "pip","uninstall", pkg.full_name.replace(":", "==")])
        # pip.main(["uninstall", pkg.full_name.replace(":", "==")])

    def clone(self, root):
        cwd = os.getcwd()
        try:
            tmp = os.path.join(root, "__tmp")
            os.makedirs(tmp)
            for path in self.__repo_cache:
                dest = os.path.join(tmp, path)
                dirn = os.path.split(dest)[0]
                if not os.path.exists(dirn):
                    os.makedirs(dirn)
                self.__console.info("cloning {}".format(path))
                with open(dest, "wb") as f:
                    self.__repo.download_file(path, f)
            millis = int((datetime.datetime.utcnow() - datetime.datetime(1970, 1, 1)).total_seconds() * 1000)
            zip_name = os.path.join(root, "{}_{}.zip".format(self.__repo.name, millis))
            with zipfile.ZipFile(zip_name, "w") as z:
                os.chdir(tmp)
                for r, _, fs in os.walk("."):
                    for f in fs:
                        z.write(os.path.join(r, f))
            self.__console.info("Successfully cloned repository {} to {}".format(self.__repo.name, zip_name))
        finally:
            os.chdir(cwd)
            shutil.rmtree(tmp)

    def restore(self, zip_repo, interactive=True):
        if self.__repo_cache and not self.__overwrite:
            if interactive: #pragma: no cover
                ok = self.__console.selection(
                    "Repository {} is not empty.\nDo you want to attempt to push into an existing repository? [y|n]: ".format(self.__repo.name),
                    ["y", "n"]
                )
                if ok.strip() == "y":
                    self.__overwrite = True
                else:
                    self.__console.warning("Aborting operation")
                    return False
            else:
                return False
        tmp = tempfile.mkdtemp()
        with zipfile.ZipFile(zip_repo, "r") as z:
            z.extractall(tmp)
        for r, _, fs in os.walk(tmp):
            for f in fs:
                pkg = PackageBuilder(os.path.join(r, f)).build()
                self.__console.info("restoring {}".format(f))
                self.upload(pkg, os.path.join(r, f))
        self.__console.info("Successfully restored repository {} from {}".format(self.__repo.name, zip_repo))
        return True

    def refresh_cache(self):
        self.__repo_cache = self.list_items()

    def __find_internal_requirements(self, pkg):
        res = set([])
        for req in pkg.requirements:
            if self.search(req):
                res.add(req)
        return res

    def __internal_install(self, requirements, install_dir, install_flags):
        #install the private package using pip.
        for r in requirements:
            #we have saved the temp packages using Package::full_name().replace(":,"_")
            #so let's get back our package to reference that file
            pkg = Package.from_text(r)
            pkg_dir = os.path.join(install_dir, pkg.full_name.replace(":", "_"))
            pkg_path = os.path.join(pkg_dir, os.listdir(pkg_dir)[0])
            #install first (and only) file in the pkg_directory
            self.__installer.install(pkg_path, install_flags)

    def __public_install(self, requirements, install_flags):
        for r in requirements:
            self.__installer.install(r, install_flags)



