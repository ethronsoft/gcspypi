from .mocks.mock_repository import MockRepository as Repository
from .mocks.mock_installer import MockInstaller as Installer
from ethronsoft.gcspypi.package.package_manager import PackageManager, Package
from ethronsoft.gcspypi.exceptions import InvalidParameter, InvalidState
from pkg_resources import resource_filename
import pytest
import tempfile
import shutil
import os
import hashlib

def test_init():
    pm = PackageManager(repo=Repository(), installer=Installer())
    assert [x for x in pm.list_items()] == []

def test_upload_download():
    pm = PackageManager(repo=Repository(), installer=Installer(), overwrite=False)
    pkg = Package(name="test_package", version="1.0.0", type="SOURCE")
    wrong = Package(name="test_package", version="")
    filename = resource_filename(__name__, "data/test_package-1.0.0.zip")
    with pytest.raises(InvalidParameter):
        pm.upload(wrong, filename)
    pm.upload(pkg, filename)
    pm.list_items() == [Package.repo_name(pkg, filename)]
    #expecting cache to be updated
    pm.list_items(from_cache=True) == [Package.repo_name(pkg, filename)]
    #uploading again without overwrite mode
    with pytest.raises(InvalidState):
        pm.upload(pkg, filename)
    #downloading by name
    try:
        tdir = tempfile.mkdtemp()
        #non existing
        assert not pm.download_by_name("fake", tdir)
        assert not pm.download_by_name(
            Package.repo_name(Package(name="test_package", version="2.0.0", type="SOURCE"), filename),
             tdir
        )
        #valid
        dest= pm.download_by_name(Package.repo_name(pkg, filename), tdir)
        source_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, "rb") as f:
            dest_md5.update(f.read())
        assert source_md5.hexdigest() == dest_md5.hexdigest()
    finally:
        shutil.rmtree(tdir)
    #downloading by package with version specified
    try:
        tdir = tempfile.mkdtemp()
        #non existing
        assert not pm.download(Package(name="fake", version="", type="SOURCE"), tdir, preferred_type="SOURCE")
        assert not pm.download(Package(name="test_package", version="2.0.0", type="SOURCE"), tdir, preferred_type="SOURCE")
        dest= pm.download(pkg, tdir, preferred_type="SOURCE")
        source_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, "rb") as f:
            dest_md5.update(f.read())
        assert source_md5.hexdigest() == dest_md5.hexdigest()
    finally:
        shutil.rmtree(tdir)
    #downloading by package without version specified (gets last)
    try:
        tdir = tempfile.mkdtemp()
        dest= pm.download(Package(name="test_package", version="", type="SOURCE"), tdir, preferred_type="SOURCE")
        source_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            source_md5.update(f.read())
        dest_md5 = hashlib.md5()
        with open(dest, "rb") as f:
            dest_md5.update(f.read())
        assert source_md5.hexdigest() == dest_md5.hexdigest()
    finally:
        shutil.rmtree(tdir)

def test_search():
    pm = PackageManager(repo=Repository(), installer=Installer(), overwrite=False)
    pkg = Package(name="test_package", version="1.0.0", type="SOURCE")
    filename = resource_filename(__name__, "data/test_package-1.0.0.zip")
    pm.upload(pkg, filename)
    assert pm.search("test_package") == pkg
    assert pm.search("test_package==1.0.0") == pkg
    assert pm.search("test_package>0.9.9") == pkg
    assert pm.search("test_package<1.9.9") == pkg
    assert pm.search("fake") == None
    with pytest.raises(InvalidParameter):
        #no name
        pm.search("")
    with pytest.raises(InvalidParameter):
        #no ops
        pm.search("1.0.0")

def test_remove():
    pm = PackageManager(repo=Repository(), installer=Installer(), overwrite=False)
    pkg = Package(name="test_package", version="1.0.0", type="SOURCE")
    filename = resource_filename(__name__, "data/test_package-1.0.0.zip")
    pm.upload(pkg, filename)
    pm.list_items() == [Package.repo_name(pkg, filename)]
    assert pm.remove(pkg, interactive=False)
    pm.list_items() == []
    #expecting cache to be updated
    pm.list_items(from_cache=True) == []
    #removing second time
    assert not pm.remove(pkg, interactive=False)
    #removing non existing
    assert not pm.remove(Package("some", "1.0.0"), interactive=False)

def test_remove_with_repo_error():
    repo = Repository()
    def problem(x):
        raise Exception()
    repo.delete = problem
    pm = PackageManager(repo=repo, installer=Installer(), overwrite=False)
    pkg = Package(name="test_package", version="1.0.0", type="SOURCE")
    filename = resource_filename(__name__, "data/test_package-1.0.0.zip")
    pm.upload(pkg, filename)
    assert not pm.remove(pkg, interactive=False)