from __future__ import unicode_literals #for BytesIO automatic conversion to unicode string in python 2
from .mocks.mock_repository import MockRepository as Repository
import six
import time

from io import BytesIO

def test_content():
    repo = Repository()
    repo.upload_content("object/x", "hello world")
    assert repo.exists("object/x")
    assert repo.download_content("object/x") == "hello world"

def test_file():
    repo = Repository()
    io = BytesIO("hello world".encode("utf-8"))
    repo.upload_file("object/x", io)
    assert repo.exists("object/x")
    assert repo.download_content("object/x").decode("utf-8") == "hello world"

def test_list():
    repo = Repository()
    repo.upload_content("object/x/y", "hello world")
    repo.upload_content("object/x/z", "hello world")
    assert len(repo.list("object/x")) == 2
    assert len(repo.list("object/x/y")) == 1
    assert len(repo.list("object/x/z")) == 1
    assert len(repo.list("object/x/w")) == 0

def test_metadata():
    repo = Repository()
    repo.upload_content("object/x", "hello world")
    time.sleep(0.01)
    repo.upload_content("object/y", "hello world")
    xm = repo.metadata("object/x")
    ym = repo.metadata("object/y")
    assert xm.md5 == ym.md5
    assert xm.time_created < ym.time_created
