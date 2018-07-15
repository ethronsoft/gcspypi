from .mocks.mock_repository import MockRepository as Repository
from ethronsoft.gcspypi.exceptions import InvalidParameter
from ethronsoft.gcspypi.package.package import Package 
from ethronsoft.gcspypi.utilities import queries as utils 
from ethronsoft.gcspypi.utilities.console import Console
from ethronsoft.gcspypi.package.package_manager import PackageManager 
import sys
import os
import pytest
import functools

def test_version_complete():
    assert utils.complete_version("1") == "1.0.0"
    assert utils.complete_version("1.1") == "1.1.0"
    assert utils.complete_version("1.1.1") == "1.1.1"
    assert utils.complete_version("") == "0.0.0"
    with pytest.raises(InvalidParameter):
        utils.complete_version("1.1.1.1")

def test_version_cmp(data):
    repo = Repository()
    pkg_mgr = PackageManager(repo=repo, installer=None, console=Console(exit_on_error=False))
    for syntax in ["toolkit>=1.0.3"]:
        pkg = pkg_mgr.search(syntax)
    assert utils.pkg_comp_version("1.05.0", "1.5.0") < 0
    assert utils.pkg_comp_version("1.0.15", "1.0.2") > 0
    assert utils.pkg_comp_version("10.0.0", "9.999.999") > 0

def test_cmp_bisect(data):
    for i in range(len(data)):
        assert i == utils.cmp_bisect(data, data[i], utils.pkg_comp_name_version)
    assert 0 == utils.cmp_bisect(data, Package("hello1", "0.0.0"), utils.pkg_comp_name_version)
    assert 2 == utils.cmp_bisect(data, Package("hello1", "0.0.3"), utils.pkg_comp_name_version)
    assert len(data) == utils.cmp_bisect(data, Package("hello3", "0.0.0"), utils.pkg_comp_name_version)
   
def test_lower(data):
    assert utils.lower([1,2], 0) == None
    assert utils.lower([1,2], 1) == None
    assert utils.lower([1,2], 2) == 1
    assert utils.lower([1,2], 3) == 2
    assert Package("hello1", "0.0.2") == utils.lower(data, Package("hello1", "0.0.15"), utils.pkg_comp_name_version)
    assert None == utils.lower(data, Package("hello1", "0.0.1"), utils.pkg_comp_name_version)
    assert Package("hello2", "0.1.1") == utils.lower(data, Package("hello3", "0.0.1"), utils.pkg_comp_name_version)
    

def test_floor(data):
    assert utils.floor([1,2,3], 1) == 1
    assert utils.floor([1,2,3], 2) == 2
    assert utils.floor([1,2,3], 0) == None
    assert utils.floor([1,2,3], 4) == 3
    assert utils.floor([1,2,3,5], 4) == 3
    assert Package("hello1", "0.0.1") == utils.floor(data, Package("hello1", "0.0.1"), utils.pkg_comp_name_version)
    assert None == utils.floor(data, Package("hello1", "0.0.05"), utils.pkg_comp_name_version)
    assert Package("hello1", "0.0.2") == utils.lower(data, Package("hello1", "0.0.3"), utils.pkg_comp_name_version)

def test_higher(data):
    assert utils.higher([1,2], 0) == 1
    assert utils.higher([1,2], 1) == 2
    assert utils.higher([1,2], 2) == None
    assert utils.higher([1,2], 3) == None
    assert Package("hello1", "0.0.1") == utils.higher(data, Package("hello1", "0.0.0"), utils.pkg_comp_name_version)
    assert Package("hello1", "0.1.2") == utils.higher(data, Package("hello1", "0.0.3"), utils.pkg_comp_name_version)
    assert None == utils.higher(data, Package("hello2", "0.1.1"), utils.pkg_comp_name_version)

def test_ceiling(data):
    assert utils.ceiling([1,2], 0) == 1
    assert utils.ceiling([1,2], 1) == 1
    assert utils.ceiling([1,2], 2) == 2
    assert utils.ceiling([1,2], 3) == None
    assert utils.ceiling([], -1) == None
    assert Package("hello1", "0.0.1") == utils.ceiling(data, Package("hello1", "0.0.0"), utils.pkg_comp_name_version)
    assert Package("hello1", "0.0.1") == utils.ceiling(data, Package("hello1", "0.0.1"), utils.pkg_comp_name_version)
    assert Package("hello1", "0.1.2") == utils.ceiling(data, Package("hello1", "0.0.3"), utils.pkg_comp_name_version)
    assert None == utils.ceiling(data, Package("hello3", "0.0.3"), utils.pkg_comp_name_version)

def test_range_query(data):
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", ">", "0.0.1")
    assert None == utils.pkg_range_query(data, "hello1", ">", "")
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "<=", "0.0.2")
    assert Package("hello1", "0.1.2") == utils.pkg_range_query(data, "hello1", "<=", "") #last 
    assert Package("hello1", "0.1.2") == utils.pkg_range_query(data, "hello1", ">=", "") #last 
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "==", "0.0.2")
    assert Package("hello1", "0.0.1") == utils.pkg_range_query(data, "hello1", "<", "0.0.2")
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "<", "") #second to last
    assert None == utils.pkg_range_query(data, "hello1", ">", "1.1.2")
    assert Package("hello1", "0.1.2") == utils.pkg_range_query(data, "hello1")
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "<")

    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", ">", "0.0.1", "<=","0.0.2")
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", ">", "0.0.1", "==","0.0.2")
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "<", "0.1.2", ">","0.0.1")
    assert Package("hello1", "0.0.2") == utils.pkg_range_query(data, "hello1", "<", "0.1.2", ">=","0.0.2")
    assert None == utils.pkg_range_query(data, "hello1", ">", "0.0.1", "<","0.0.2")
    assert Package("hello1", "0.0.1") == utils.pkg_range_query(data, "hello1", ">=", "0.0.1", "<","0.0.2")
    assert None == utils.pkg_range_query(data, "hello1", ">", "0.0.1", "<", "0.0.1")

    with pytest.raises(InvalidParameter):
        utils.pkg_range_query(data, "hello1", "wrong-op")
    with pytest.raises(InvalidParameter):
        utils.pkg_range_query(data, "hello1", ">", "0.0.1", "wrong-op", "0.0.2")

def test_get_type():
    assert utils.get_package_type("something.zip") == "SOURCE"
    assert utils.get_package_type("something.tar") == "SOURCE"
    assert utils.get_package_type("something.tar.gz") == "SOURCE"
    assert utils.get_package_type("something.whl") == "WHEEL"
    with pytest.raises(InvalidParameter):
        utils.get_package_type("wrong")

def test_version_sorting():
    versions = [
        "1.0.0",
        "1.0.05",
        "0.1.0",
        "1.1.1",
        "0.0.1",
        "1.01.1"
    ]
    versions.sort(key=functools.cmp_to_key(utils.pkg_comp_version))
    assert versions == [
        "0.0.1",
        "0.1.0",
        "1.0.0",
        "1.0.05",
        "1.01.1",
        "1.1.1"
    ]    

def test_items_to_package():
    items = [
        "some/1.1.0/filename.zip",
        "some/1.1.0/filename.zip",
        "some/1.0.0/filename.zip",
        "some/2.0.0/filename.zip",
        "other/3.0.0/filename.zip",
        "other/1.0.0/filename.zip",
    ]
    assert [p.full_name for p in utils.items_to_package(items, unique=False)] == [
        "other:1.0.0",
        "other:3.0.0",
        "some:1.0.0",
        "some:1.1.0",
        "some:1.1.0",
        "some:2.0.0",
    ]
    assert [p.full_name for p in utils.items_to_package(items, unique=True)] == [
        "other:1.0.0",
        "other:3.0.0",
        "some:1.0.0",
        "some:1.1.0",
        "some:2.0.0",
    ]

@pytest.fixture
def data():
    return [
        Package("hello1", "0.0.1"),
        Package("hello1", "0.0.2"),
        Package("hello1", "0.1.2"),
        Package("hello2", "0.1.0"),
        Package("hello2", "0.1.1"),
    ]
