from ethronsoft.gcspypi.package.package import Package
from ethronsoft.gcspypi.exceptions import InvalidParameter, InvalidState
import pytest

def test_repo_name():
    p = Package("some", "1.0.0")
    assert p.full_name == "some:1.0.0"
    wrong = Package("some", "")
    assert Package.repo_name(p, "/some/filename.txt") == "some/1.0.0/filename.txt"
    with pytest.raises(InvalidState):
        Package.repo_name(wrong, "/some/filename.txt") 

def test_equality():
    p1 = Package("some", "1.0.0", type="A")
    p2 = Package("some", "1.0.0", type="A")
    p3 = Package("some", "1.0.0", type="B")
    p4 = Package("some", "", type="A")
    p5 = Package("other", "1.0.0", type="A")
    p6 = Package("other", "1.0.0", type="B")
    
    assert p1.full_name == str(p1)
    assert p1 == p2
    assert hash(p1) == hash(p2)
    assert p1 != p3
    assert hash(p1) != hash(p3) 
    assert p1 != p4
    assert p2 != p5
    assert p5 != p6


def test_from_text():
    with pytest.raises(InvalidParameter):
        Package.from_text("some>1.0.0")
    with pytest.raises(InvalidParameter):
        Package.from_text("some<1.0.0")
    with pytest.raises(InvalidParameter):
        Package.from_text("some<=1.0.0")
    with pytest.raises(InvalidParameter):
        Package.from_text("some>=1.0.0")
    
    assert Package.from_text("some==1.0.0") == Package("some", "1.0.0")
    assert Package.from_text("some==") == Package("some", "")
    assert Package.from_text("some") == Package("some", "")