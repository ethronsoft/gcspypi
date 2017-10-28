import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__),"../ethronsoft/gcspypi"))
from pb import *

class PackageBuilderTest(unittest.TestCase):

    def test_src(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        pkg = PackageBuilder(os.path.join(dir,"data","dist","test_package-1.0.0.tar.gz")).build()
        self.assertEqual(pkg.name, "test-package")
        self.assertEqual(pkg.version, "1.0.0")
        self.assertEqual(pkg.requirements, set(["test-dep1", "test-dep2"]))
        self.assertEqual(pkg.type, "SOURCE")

    def test_wheel(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        pkg = PackageBuilder(os.path.join(dir,"data","dist","test_package-1.0.0-py2-none-any.whl")).build()
        self.assertEqual(pkg.name, "test-package")
        self.assertEqual(pkg.version, "1.0.0")
        self.assertEqual(pkg.requirements, set(["test-dep1", "test-dep2"]))
        self.assertEqual(pkg.type, "WHEEL")

if __name__ == "__main__":
    unittest.main()