import tarfile
import zipfile
import shutil
import os
import glob
import json
import tempfile


class Package(object):
    def __init__(self, name, version="", requirements=set([])):
        self.__name = name.replace("_", "-")
        self.__version = self.__checked_version(version) if version else ""
        self.__requirements = set([])
        for r in requirements:
            self.__requirements.add(r.replace("_","-"))

    @staticmethod
    def from_text(text):
        return Package("some")

    def __checked_version(self, v):
        if (len(v.split(".")) != 3): raise Exception("Version must be provided in major.minor.patch format")
        return v

    def __eq__(self, o):
        return isinstance(o, Package) and self.name == o.name and self.version == o.version

    def __hash__(self):
        return hash(self.full_name)

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
        return self.__version


class PackageBuilder(object):
    def __init__(self, raw_package):
        try:
            cwd = os.getcwd()
            dir = tempfile.mkdtemp()
            os.chdir(dir)
            if ".zip" in raw_package:
                with zipfile.ZipFile(raw_package, "r") as f:
                    self.__info = self.__extract_source(f)
            elif ".tar" in raw_package:
                with tarfile.open(raw_package, "r") as f:
                    self.__info = self.__extract_source(f)
            elif ".egg" in raw_package:
                with zipfile.ZipFile(raw_package, "r") as f:
                    self.__info = self.__extract_egg(f)
            elif ".whl" in raw_package:
                with zipfile.ZipFile(raw_package, "r") as f:
                    self.__info = self.__extract_wheel(f)
            else:
                raise Exception("Unrecognized file extension. expected {.zip|.tar*|.egg|.whl}")
        finally:
            os.chdir(cwd)
            shutil.rmtree(dir)

    def __seek_and_apply(self, zip, target, command):
        zip.extractall(".")
        for r, dir, f in os.walk("."):
            for x in f:
                if target in x:
                    with open(os.path.join(r, x), "r") as target_file:
                        command(target_file)
                    return

    def __extract_egg(self, zip):
        # egg needs to get data from PKG-INFO, just like source...
        return self.__extract_source(zip)

    def __extract_source(self, zip):
        class InfoCmd(object):
            def __init__(self):
                self.metadata = {}

            def __call__(self, target):
                map = {}
                for line in target.readlines():
                    k, v = line.split(":")
                    map[k.upper().strip()] = v.strip()
                self.metadata["name"] = map["name".upper()]
                self.metadata["version"] = map["version".upper()]

        cmd = InfoCmd()
        self.__seek_and_apply(zip, "PKG-INFO", cmd)
        if not cmd.metadata:
            raise Exception("Could not find PKG-INFO")
        return {"name": cmd.metadata["name"],
                "version": cmd.metadata["version"],
                "requirements": self.__read_requirements(zip)}

    def __extract_wheel(self, zip):
        class InfoCmd(object):
            def __init__(self):
                self.metadata = {}

            def __call__(self, target):
                map = json.loads(target.read())
                self.metadata["name"] = map["name"]
                self.metadata["version"] = map["version"]
                self.metadata["requirements"] = set([])
                for reqs in map["run_requires"]:
                    self.metadata["requirements"].update(reqs["requires"])

        cmd = InfoCmd()
        self.__seek_and_apply(zip, "metadata.json", cmd)
        if not cmd.metadata:
            raise Exception("Could not find PKG-INFO")
        return cmd.metadata

    def __read_requirements(self, zip):
        class RequiresCmd(object):
            def __init__(self):
                self.requires = []

            def __call__(self, target):
                self.requires = [x for x in target.read().splitlines()]

        cmd = RequiresCmd()
        self.__seek_and_apply(zip, "requires", cmd)
        return cmd.requires

    def build(self):
        return Package(self.__info["name"], self.__info["version"], set(self.__info["requirements"]))
