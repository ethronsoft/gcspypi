import sys
import os
import unittest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ethronsoft.gcspypi import pb 
from ethronsoft.gcspypi import utils 
from ethronsoft.gcspypi import pm 

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.data = [
            pb.Package("hello1", "0.0.1"),
            pb.Package("hello1", "0.0.2"),
            pb.Package("hello1", "0.1.2"),
            pb.Package("hello2", "0.1.0"),
            pb.Package("hello2", "0.1.1"),
        ]

    def test_version_cmp(self):
        pkg_mgr = pm.PackageManager("ethronsoft-pypi")
        for syntax in ["toolkit>=1.0.3"]:
            pkg = pkg_mgr.search(syntax)
            print(pkg)
        self.assertLess(utils.pkg_comp_version("1.05.0", "1.5.0"), 0)
        self.assertGreater(utils.pkg_comp_version("1.0.15", "1.0.2"), 0)
        self.assertGreater(utils.pkg_comp_version("10.0.0", "9.999.999"), 0)

    def test_cmp_bisect(self):
        for i in range(len(self.data)):
            self.assertEqual(i, utils.cmp_bisect(self.data, self.data[i], utils.pkg_comp_name_version))
        self.assertEqual(0, utils.cmp_bisect(self.data, pb.Package("hello1", "0.0.0"), utils.pkg_comp_name_version))
        self.assertEqual(2, utils.cmp_bisect(self.data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version))
        self.assertEqual(len(self.data), utils.cmp_bisect(self.data, pb.Package("hello3", "0.0.0"), utils.pkg_comp_name_version))

    def test_lower(self):
        self.assertEqual(pb.Package("hello1", "0.0.2"),
                         utils.lower(self.data, pb.Package("hello1", "0.0.15"), utils.pkg_comp_name_version))
        self.assertEqual(None,
                         utils.lower(self.data, pb.Package("hello1", "0.0.1"), utils.pkg_comp_name_version))
        self.assertEqual(pb.Package("hello2", "0.1.1"),
                         utils.lower(self.data, pb.Package("hello3", "0.0.1"), utils.pkg_comp_name_version))

    def test_floor(self):
        self.assertEqual(pb.Package("hello1", "0.0.1"),
                         utils.floor(self.data, pb.Package("hello1", "0.0.1"), utils.pkg_comp_name_version))
        self.assertEqual(None,
                         utils.floor(self.data, pb.Package("hello1", "0.0.05"), utils.pkg_comp_name_version))
        self.assertEqual(pb.Package("hello1", "0.0.2"),
                         utils.lower(self.data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version))

    def test_higher(self):
        self.assertEqual(pb.Package("hello1", "0.0.1"),
                         utils.higher(self.data, pb.Package("hello1", "0.0.0"), utils.pkg_comp_name_version))
        self.assertEqual(pb.Package("hello1", "0.1.2"),
                         utils.higher(self.data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version))
        self.assertEqual(None,
                         utils.higher(self.data, pb.Package("hello2", "0.1.1"), utils.pkg_comp_name_version))

    def test_ceiling(self):
        self.assertEqual(pb.Package("hello1", "0.0.1"),
                         utils.ceiling(self.data, pb.Package("hello1", "0.0.0"), utils.pkg_comp_name_version))
        self.assertEqual(pb.Package("hello1", "0.0.1"),
                         utils.ceiling(self.data, pb.Package("hello1", "0.0.1"), utils.pkg_comp_name_version))
        self.assertEqual(pb.Package("hello1", "0.1.2"),
                         utils.ceiling(self.data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version))
        self.assertEqual(None,
                         utils.ceiling(self.data, pb.Package("hello3", "0.0.3"), utils.pkg_comp_name_version))

    def test_range_query(self):
        self.assertEqual(pb.Package("hello1", "0.0.2"),
                         utils.pkg_range_query(self.data, "hello1", ">", "0.0.1"))
        self.assertEqual(pb.Package("hello1", "0.0.2"),
                         utils.pkg_range_query(self.data, "hello1", ">", "0.0.1", "<=","0.0.2"))
        self.assertEqual(None,
                         utils.pkg_range_query(self.data, "hello1", ">", "0.0.1", "<","0.0.2"))
        self.assertEqual(pb.Package("hello1", "0.0.1"),
                         utils.pkg_range_query(self.data, "hello1", ">=", "0.0.1", "<","0.0.2"))
        self.assertEqual(None,
                         utils.pkg_range_query(self.data, "hello1", ">", "0.0.1", "<", "0.0.1"))
        self.assertEqual(pb.Package("hello1", "0.0.2"),
                         utils.pkg_range_query(self.data, "hello1", "==", "0.0.2"))
        self.assertEqual(pb.Package("hello1", "0.0.1"),
                         utils.pkg_range_query(self.data, "hello1", "<", "0.0.2"))
        self.assertEqual(None,
                         utils.pkg_range_query(self.data, "hello1", ">", "1.1.2"))
        self.assertEqual(pb.Package("hello1", "0.1.2"),
                         utils.pkg_range_query(self.data, "hello1"))
        self.assertEqual(pb.Package("hello1", "0.0.2"),
                         utils.pkg_range_query(self.data, "hello1", "<"))


if __name__ == '__main__':
    unittest.main()