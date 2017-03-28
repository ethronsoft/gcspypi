import os
import unittest
import sys
sys.path.append("../gcspypi")
from gcspypi.pb import *


class PackageBuilderTest(unittest.TestCase):

    def test_src(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        pkg = PackageBuilder(os.path.join(dir,"data","dist","test_package-1.0.0.tar.gz")).build()
        self.assertEqual(pkg.name, "test-package")
        self.assertEqual(pkg.version, "1.0.0")
        self.assertEqual(pkg.requirements, set(["test-dep1", "test-dep2"]))

    def test_wheel(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        pkg = PackageBuilder(os.path.join(dir,"data","dist","test_package-1.0.0-py2-none-any.whl")).build()
        self.assertEqual(pkg.name, "test-package")
        self.assertEqual(pkg.version, "1.0.0")
        self.assertEqual(pkg.requirements, set(["test-dep1", "test-dep2"]))

    def test_egg(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        pkg = PackageBuilder(os.path.join(dir,"data","dist","test_package-1.0.0-py2.7.egg")).build()
        self.assertEqual(pkg.name, "test-package")
        self.assertEqual(pkg.version, "1.0.0")
        self.assertEqual(pkg.requirements, set(["test-dep1", "test-dep2"]))


if __name__ == "__main__":
    unittest.main()