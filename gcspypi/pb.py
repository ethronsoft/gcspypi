import zipfile
import shutil
import os
import glob
import json
import tempfile


class Package(object):
    def __init__(self, name, version, requirements):
        self.__name = name
        self.__version = self.__checked_version(version) if version else ""
        self.__requirements = requirements

    @staticmethod
    def from_text(text):
        return Package("some")

    def __checked_version(self, v):
        if (len(v.split(".")) != 3): raise Exception("Version must be provided in major.minor.patch format")
        return v

    def __del__(self):
        print "Package destructor"

    def prepare(self):
        return "some"

    @property
    def name(self):
        return self.__name

    @property
    def full_name(self):
        return self.name + ":" + self.version if (self.version != "") else self.name

    @property
    def requirements(self):
        return self.__requirements

    @property
    def version(self):
        return self.__name


class PackageBuilder(object):
    def __init__(self, raw_package):
        if ".zip" in raw_package or ".tar" in raw_package:
            self.__info = self.__extract_source(raw_package)
        elif ".egg" in raw_package:
            self.__info = self.__extract_egg(raw_package)
        elif ".whl" in raw_package:
            self.__info = self.__extract_wheel(raw_package)
        else:
            raise Exception("Unrecognized file extension. expected {.zip|.tar|.tar.gz|.egg|.whl}")

    def __seek_and_apply(self, raw_package, target, command):
        try:
            cwd = os.getcwd()
            dir = tempfile.mkdtemp()
            os.chdir(dir)
            with zipfile.ZipFile(raw_package, "r") as f:
                f.extractall(".")
                for r, dir, f in os.walk("."):
                    if f == target:
                        with open(os.path.join(r, file), "r") as target_file:
                            command(target_file)
                        break
        finally:
            shutil.rmtree(dir)
            os.chdir(cwd)

    def __extract_egg(self, raw_package):
        # egg needs to get data from PKG-INFO, just like source...
        return self.__extract_source(raw_package)

    def __extract_source(self, raw_package):
        class InfoCmd(object):
            def __init__(self):
                self.metadata = {}

            def __call__(self, target):
                map = {}
                for line in target.readlines():
                    k, v = line.split(":")
                    map[k] = v
                self.metadata["name"] = map["name"]
                self.metadata["version"] = map["version"]

        cmd = InfoCmd()
        self.__seek_and_apply(raw_package, "PKG-INFO", cmd)
        if not cmd.metadata:
            raise Exception("Could not find PKG-INFO in: " + raw_package)
        requirements = self.__read_requirements(raw_package)
        return {"name": cmd.metadata.name, "version": cmd.metadata.version, "requirements": requirements}

    def __extract_wheel(self, raw_package):
        class InfoCmd(object):
            def __init__(self):
                self.metadata = {}

            def __call__(self, target):
                map = json.loads(target.read())
                self.metadata["name"] = map["name"]
                self.metadata["version"] = map["version"]

        cmd = InfoCmd()
        self.__seek_and_apply(raw_package, "metadata.json", cmd)
        if not cmd.metadata:
            raise Exception("Could not find PKG-INFO in: " + raw_package)
        requirements = self.__read_requirements(raw_package)
        return {"name": cmd.metadata.name, "version": cmd.metadata.version, "requirements": requirements}

    def __read_requirements(self, raw_package):
        class RequiresCmd(object):
            def __init__(self):
                self.requires = []

            def __call__(self, target):
                self.requires = target.readlines()

        cmd = RequiresCmd()
        self.__seek_and_apply(raw_package, "requires", cmd)
        return cmd.requires

    def build(self):
        return Package(self.__info.name, self.__info.version, set(self.__info.requirements))
