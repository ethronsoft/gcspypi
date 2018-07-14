from ethronsoft.gcspypi.package.package_builder import PackageBuilder
from ethronsoft.gcspypi.exceptions import InvalidState
from pkg_resources import resource_filename
import os
import sys
import pytest

def test_src_tar():
    pkg_path = resource_filename(__name__, "data/test_package-1.0.0.tar.gz")
    pkg = PackageBuilder(pkg_path).build()
    assert pkg.name == "test-package"
    assert pkg.version == "1.0.0"
    assert pkg.requirements == set(["test-dep1", "test-dep2"])
    assert pkg.type == "SOURCE"

def test_src_wrong():
    pkg_path = resource_filename(__name__, "data/WRONG-test_package-1.0.0.zip")
    with pytest.raises(InvalidState):
        PackageBuilder(pkg_path).build()

def test_wheel_wrong():
    pkg_path = resource_filename(__name__, "data/WRONG-test_package-1.0.0-py2-none-any.whl")
    with pytest.raises(InvalidState):
        PackageBuilder(pkg_path).build()

def test_src_zip():
    pkg_path = resource_filename(__name__, "data/test_package-1.0.0.zip")
    pkg = PackageBuilder(pkg_path).build()
    assert pkg.name == "test-package"
    assert pkg.version == "1.0.0"
    assert pkg.requirements == set(["test-dep1", "test-dep2"])
    assert pkg.type == "SOURCE"

def test_wheel():
    pkg_path = resource_filename(__name__, "data/test_package-1.0.0-py2-none-any.whl")
    pkg = PackageBuilder(pkg_path).build()
    assert pkg.name == "test-package"
    assert pkg.version == "1.0.0"
    assert pkg.requirements == set(["test-dep1", "test-dep2"])
    assert pkg.type == "WHEEL"
