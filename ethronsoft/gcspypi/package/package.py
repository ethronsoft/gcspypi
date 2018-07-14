from ethronsoft.gcspypi.utilities.version import complete_version
from ethronsoft.gcspypi.exceptions import InvalidState, InvalidParameter
# from functools import total_ordering
import os


# @total_ordering
# class Version(object):
#     """Packages support the following versioning scheme:

#      <major>.<minor>.<patch>

#      where all <token>s are integers
#     """

#     @staticmethod
#     def from_string(version_string):
#         """returns a Version instance from a __str__ representation.

#            Any empty <token> is replaced by a 0

#         Arguments:
#             version_string {str} -- The string representation of a version. See __str__()

#         Returns:
#             Version -- new Version instance
#         """
#         tokens = version_string.split(".")
#         version_tokens = [0, 0, 0]
#         for i in range(min(len(tokens), 3)):
#             version_tokens[i] = int(tokens[i]) if tokens[i] else 0
#         return Version(*version_tokens)

#     def __str__(self):
#         return "{major}.{minor}.{patch}".format(major=self.major, minor=self.minor, patch=self.patch)

#     def __init__(self, major, minor, patch):
#         self.major = major
#         self.minor = minor
#         self.patch = patch

#     def __eq__(self, o):
#         return (o.major, o.minor, o.patch) == (self.major, self.minor, self.patch)

#     def __lt__(self, o):
#         if self.major > o.major:
#             return False
#         elif self.major < o.major:
#             return True
#         else:  # major equal
#             if self.minor > o.minor:
#                 return False
#             elif self.minor < o.minor:
#                 return True
#             else:  # minor equal
#                 if self.patch > o.patch:
#                     return False
#                 elif self.patch < o.patch:
#                     return True
#                 else:  # patch equal
#                     return False

#     def __cmp__(self, o):
#         if self < o:
#             return -1
#         elif self > o:
#             return 1
#         else:
#             return 0


class Package(object):

    def __init__(self, name, version="", requirements=set([]), type=""):
        self.name = name.replace("_", "-")
        self.version = complete_version(version) if version else None
        self.requirements = set([])
        self.type = type
        for r in requirements:
            self.requirements.add(r.replace("_","-"))

    @staticmethod
    def repo_name(pkg, filename):
        if not pkg.version:
            raise InvalidState("cannot formulate package repository-name for a package without version")
        return "{name}/{version}/{filename}".format(
            name=pkg.name,
            version=pkg.version,
            filename=os.path.split(filename)[1]
        )

    @staticmethod
    def from_text(text):
        if ">" in text or "<" in text:
            raise InvalidParameter("Cannot create a package with non deterministic version")
        if "==" in text:
            name, version = text.split("==")
            return Package(name.strip(), version.strip())
        else:
            return Package(text)

    def __str__(self):
        return self.full_name

    def __repr__(self): # pragma: no cover
        return "<Package {}>".format(str(self))

    def __eq__(self, o):
        if not o: return False
        return (self.name, self.version, self.type) == (o.name, o.version, o.type)

    def __ne__(self, o):
        return not self.__eq__(o)

    def __hash__(self):
        return hash((self.name, str(self.version), self.type))

    @property
    def full_name(self):
        return self.name + ":" + self.version if self.version else self.name
