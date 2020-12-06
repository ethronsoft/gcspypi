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

def test_wheel_py3():
    pkg_path = resource_filename(__name__, "data/gcspypi-1.0.8+dev1-py3-none-any.whl")
    pkg = PackageBuilder(pkg_path).build()
    assert pkg.name == "gcspypi"
    assert pkg.version == "1.0.8+dev1"
    assert pkg.type == "WHEEL"
    assert pkg.requirements == set(["colorama (>=0.4.1)",
                                    "google-cloud-storage (>=1.23.0)",
                                    "six (>=1.12.0)",
                                    "tqdm (>=4.32.0)", ])
