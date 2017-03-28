import unittest
import sys
sys.path.append("../gcspypi")
from gcspypi.pb import Package
from gcspypi.utils import *

class TestUtils(unittest.TestCase):

    def setUp(self):
        self.data = [
            Package("hello1", "0.0.1"),
            Package("hello1", "0.0.2"),
            Package("hello1", "0.1.2"),
            Package("hello2", "0.1.0"),
            Package("hello2", "0.1.1"),
        ]

    def test_cmp_bisect(self):
        for i in range(len(self.data)):
            self.assertEqual(i, cmp_bisect(self.data, self.data[i], pkg_comp_name_version))
        self.assertEqual(0, cmp_bisect(self.data, Package("hello1", "0.0.0"), pkg_comp_name_version))
        self.assertEqual(2, cmp_bisect(self.data, Package("hello1", "0.0.3"), pkg_comp_name_version))
        self.assertEqual(len(self.data), cmp_bisect(self.data, Package("hello3", "0.0.0"), pkg_comp_name_version))

    def test_lower(self):
        self.assertEqual(Package("hello1", "0.0.1"),
                         lower(self.data, Package("hello1", "0.0.15"), pkg_comp_name_version))
        self.assertEqual(None,
                         lower(self.data, Package("hello1", "0.0.1"), pkg_comp_name_version))
        self.assertEqual(Package("hello2", "0.1.1"),
                         lower(self.data, Package("hello3", "0.0.1"), pkg_comp_name_version))

    def test_floor(self):
        self.assertEqual(Package("hello1", "0.0.1"),
                         floor(self.data, Package("hello1", "0.0.1"), pkg_comp_name_version))
        self.assertEqual(None,
                         floor(self.data, Package("hello1", "0.0.05"), pkg_comp_name_version))
        self.assertEqual(Package("hello1", "0.0.2"),
                         lower(self.data, Package("hello1", "0.0.3"), pkg_comp_name_version))

    def test_higher(self):
        self.assertEqual(Package("hello1", "0.0.1"),
                         higher(self.data, Package("hello1", "0.0.0"), pkg_comp_name_version))
        self.assertEqual(Package("hello1", "0.1.2"),
                         higher(self.data, Package("hello1", "0.0.3"), pkg_comp_name_version))
        self.assertEqual(None,
                         higher(self.data, Package("hello2", "0.1.1"), pkg_comp_name_version))

    def test_ceiling(self):
        self.assertEqual(Package("hello1", "0.0.1"),
                         ceiling(self.data, Package("hello1", "0.0.0"), pkg_comp_name_version))
        self.assertEqual(Package("hello1", "0.0.1"),
                         ceiling(self.data, Package("hello1", "0.0.1"), pkg_comp_name_version))
        self.assertEqual(Package("hello1", "0.1.2"),
                         ceiling(self.data, Package("hello1", "0.0.3"), pkg_comp_name_version))
        self.assertEqual(None,
                         ceiling(self.data, Package("hello3", "0.0.3"), pkg_comp_name_version))

    def test_range_query(self):
        self.assertEqual(Package("hello1", "0.0.2"),
                         pkg_range_query(self.data, "hello1", ">", "0.0.1"))
        self.assertEqual(Package("hello1", "0.0.2"),
                         pkg_range_query(self.data, "hello1", ">", "0.0.1", "<=","0.0.2"))
        self.assertEqual(None,
                         pkg_range_query(self.data, "hello1", ">", "0.0.1", "<","0.0.2"))
        self.assertEqual(Package("hello1", "0.0.1"),
                         pkg_range_query(self.data, "hello1", ">=", "0.0.1", "<","0.0.2"))
        self.assertEqual(None,
                         pkg_range_query(self.data, "hello1", ">", "0.0.1", "<", "0.0.1"))
        self.assertEqual(Package("hello1", "0.0.2"),
                         pkg_range_query(self.data, "hello1", "==", "0.0.2"))
        self.assertEqual(Package("hello1", "0.0.1"),
                         pkg_range_query(self.data, "hello1", "<", "0.0.2"))
        self.assertEqual(None,
                         pkg_range_query(self.data, "hello1", ">", "1.1.2"))
        self.assertEqual(Package("hello1", "0.1.2"),
                         pkg_range_query(self.data, "hello1"))
        self.assertEqual(Package("hello1", "0.0.2"),
                         pkg_range_query(self.data, "hello1", "<"))

if __name__ == '__main__':
    unittest.main()