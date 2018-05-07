import sys
import os
import pytest

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ethronsoft.gcspypi import pb 
from ethronsoft.gcspypi import utils 
from ethronsoft.gcspypi import pm 

@pytest.fixture
def data():
    return [
        pb.Package("hello1", "0.0.1"),
        pb.Package("hello1", "0.0.2"),
        pb.Package("hello1", "0.1.2"),
        pb.Package("hello2", "0.1.0"),
        pb.Package("hello2", "0.1.1"),
    ]

def test_version_cmp(data):
    pkg_mgr = pm.PackageManager("ethronsoft-pypi")
    for syntax in ["toolkit>=1.0.3"]:
        pkg = pkg_mgr.search(syntax)
        print(pkg)
    assert utils.pkg_comp_version("1.05.0", "1.5.0") < 0
    assert utils.pkg_comp_version("1.0.15", "1.0.2") > 0
    assert utils.pkg_comp_version("10.0.0", "9.999.999") > 0

def test_cmp_bisect(data):
    for i in range(len(data)):
        assert i == utils.cmp_bisect(data, data[i], utils.pkg_comp_name_version)
    assert 0 == utils.cmp_bisect(data, pb.Package("hello1", "0.0.0"), utils.pkg_comp_name_version)
    assert 2 == utils.cmp_bisect(data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version)
    assert len(data) == utils.cmp_bisect(data, pb.Package("hello3", "0.0.0"), utils.pkg_comp_name_version)
   
def test_lower(data):
    assert pb.Package("hello1", "0.0.2") == utils.lower(data, pb.Package("hello1", "0.0.15"), utils.pkg_comp_name_version)
    assert None == utils.lower(data, pb.Package("hello1", "0.0.1"), utils.pkg_comp_name_version)
    assert pb.Package("hello2", "0.1.1") == utils.lower(data, pb.Package("hello3", "0.0.1"), utils.pkg_comp_name_version)
    

def test_floor(data):
    assert pb.Package("hello1", "0.0.1") == utils.floor(data, pb.Package("hello1", "0.0.1"), utils.pkg_comp_name_version)
    assert None == utils.floor(data, pb.Package("hello1", "0.0.05"), utils.pkg_comp_name_version)
    assert pb.Package("hello1", "0.0.2") == utils.lower(data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version)

def test_higher(data):
    assert pb.Package("hello1", "0.0.1") == utils.higher(data, pb.Package("hello1", "0.0.0"), utils.pkg_comp_name_version)
    assert pb.Package("hello1", "0.1.2") == utils.higher(data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version)
    assert None == utils.higher(data, pb.Package("hello2", "0.1.1"), utils.pkg_comp_name_version)

def test_ceiling(data):
    assert pb.Package("hello1", "0.0.1") == utils.ceiling(data, pb.Package("hello1", "0.0.0"), utils.pkg_comp_name_version)
    assert pb.Package("hello1", "0.0.1") == utils.ceiling(data, pb.Package("hello1", "0.0.1"), utils.pkg_comp_name_version)
    assert pb.Package("hello1", "0.1.2") == utils.ceiling(data, pb.Package("hello1", "0.0.3"), utils.pkg_comp_name_version)
    assert None == utils.ceiling(data, pb.Package("hello3", "0.0.3"), utils.pkg_comp_name_version)

def test_range_query(data):
    assert pb.Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", ">", "0.0.1")
    assert pb.Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", ">", "0.0.1", "<=","0.0.2")
    assert None == utils.pkg_range_query(data, "hello1", ">", "0.0.1", "<","0.0.2")
    assert pb.Package("hello1", "0.0.1") == utils.pkg_range_query(data, "hello1", ">=", "0.0.1", "<","0.0.2")
    assert None == utils.pkg_range_query(data, "hello1", ">", "0.0.1", "<", "0.0.1")
    assert pb.Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "==", "0.0.2")
    assert pb.Package("hello1", "0.0.1") == utils.pkg_range_query(data, "hello1", "<", "0.0.2")
    assert None == utils.pkg_range_query(data, "hello1", ">", "1.1.2")
    assert pb.Package("hello1", "0.1.2") == utils.pkg_range_query(data, "hello1")
    assert pb.Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "<")


