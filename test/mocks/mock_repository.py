from ethronsoft.gcspypi.exceptions import RepositoryError, NotFound
from ethronsoft.gcspypi.repository.object_metadata import ObjectMetadata
import hashlib
import datetime

def _make_metadata(content, content_type):
    return ObjectMetadata(content_type, hashlib.md5(content).hexdigest(), datetime.datetime.now())

class MockRepository(object):
    
    def __init__(self):
        self.name = "mock_repo"
        self._repository = {

        }

    def upload_content(self, object_name, content, content_type="text/plain"):
       self._repository[object_name] = {
           "content": content,
           "metadata": _make_metadata(content.encode("utf-8"), content_type)
       }

    def upload_file(self,object_name, file_obj):
        cnt = file_obj.read()
        self._repository[object_name] = {
           "content": cnt,
           "metadata": _make_metadata(cnt, "application/octet-stream")
        }

    def download_content(self, object_name):
        if not self.exists(object_name):
            raise NotFound()
        return self._repository[object_name]["content"]

    def download_file(self, object_name, file_obj):
        if not self.exists(object_name):
            raise NotFound()
        file_obj.write(self._repository[object_name]["content"])

    def delete(self, object_name):
        if self.exists(object_name):
           del self._repository[object_name]

    def exists(self, object_name):
       return object_name in self._repository

    def metadata(self, object_name):
        if not self.exists(object_name):
            raise NotFound()
        return self._repository[object_name]["metadata"]

    def list(self, prefix=""):
        return list(filter(lambda x: x.startswith(prefix) ,self._repository.keys()))
