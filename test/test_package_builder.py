import os
import sys
import unittest
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from ethronsoft.gcspypi import pb

DIR = os.path.dirname(os.path.abspath(__file__))

def test_src():
    pkg = pb.PackageBuilder(os.path.join(DIR,"data","test_package-1.0.0.tar.gz")).build()
    assert pkg.name == "test-package"
    assert pkg.version == "1.0.0"
    assert pkg.requirements == set(["test-dep1", "test-dep2"])
    assert pkg.type == "SOURCE"

def test_wheel():
    pkg = pb.PackageBuilder(os.path.join(DIR,"data","test_package-1.0.0-py2-none-any.whl")).build()
    assert pkg.name == "test-package"
    assert pkg.version == "1.0.0"
    assert pkg.requirements == set(["test-dep1", "test-dep2"])
    assert pkg.type == "WHEEL"
