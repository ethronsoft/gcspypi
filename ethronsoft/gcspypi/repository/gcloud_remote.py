from google.cloud import storage
from ethronsoft.gcspypi.exceptions import RepositoryError, NotFound
from .object_metadata import ObjectMetadata
import six
import sys
import warnings


class GCloudRepository(object):

    def __init__(self, bucket):
        """GCloudRepository constructor

        Arguments:
            bucket {str} -- The Google Cloud Storage Bucket to act as our repository

        Raises:
            cpm.exceptions.RepositoryError -- If the was an error connecting to the repository
            or to the bucket. Most often due to invalid credentials    
        """
        try:
            #NOTE: It is convenient to authenticate with application-default credentials.
            #Moving away from it is as simple as setting an environment variable and getting access
            #to server credentials but this is cumbersome for the front-end use of cpm.
            #Keeping this for as long as google doesn't deprecate feature
            warnings.filterwarnings("ignore", "Your application has authenticated using end user credentials")
            self.bucket = storage.Client().bucket(bucket)
            if not self.bucket.exists():
                raise RepositoryError("{} does not exist".format(bucket))
            self.name = bucket
        except Exception as e:
            six.raise_from(RepositoryError, e)

    def upload_content(self, object_name, content, content_type="text/plain"):
        """Uploads the content to the repository, targetting object `object`

        Arguments:
            content {str} -- The Content as a string
            object_name {str} -- The name of the object to create/replace in the repository
            content_type {str} -- The MIME Type for the Content (defaults to 'text/plain')

        Raises:
            cpm.exceptions.RepositoryError -- If the was an error during the upload
        """
        try:
            blob = self.bucket.blob(object_name)
            blob.upload_from_string(content, content_type)
        except Exception as e:
            six.raise_from(RepositoryError(str(e)), e)

    def upload_file(self, object_name, file_obj):
        """Uploads the file to the repository, targetting object `object`

        Arguments:
            file_obj {file} -- The file to upload
            object_name {str} -- The name of the object to create/replace in the repository

        Raises:
            cpm.exceptions.RepositoryError -- If the was an error during the upload
        """
        try:
            blob = self.bucket.blob(object_name)
            blob.upload_from_file(file_obj)
        except Exception as e:
            six.raise_from(RepositoryError(str(e)), e)

    def download_content(self, object_name):
        """Download the content of object_name as a string

        Arguments:
            object_name {str} -- Name of object to download

        Raises:
            cpm.exceptions.NotFound -- If the object_name does not exist

        Returns:
            str -- Content as string
        """
        blob = self.bucket.blob(object_name)
        try:
            return blob.download_as_string()
        except Exception as e:
            six.raise_from(RepositoryError(str(e)), e)

    def download_file(self, object_name, file_obj):
        """Download the object_name to a file `file_name`

        Arguments:
            object_name {str} -- Name of object to download
            file_obj {file} -- File object to write into

        Raises:
            cpm.exceptions.NotFound -- If the object_name does not exist    
        """
        blob = self.bucket.blob(object_name)
        try:
            return blob.download_to_file(file_obj)
        except Exception as e:
            six.raise_from(NotFound(str(e)), e)

    def delete(self, object_name):
        """Attempt to delete object `object_name`

        Arguments:
           object_name {str} -- Name of object to delete

        Returns:
            bool -- flag for succesful deletion
        """

        blob = self.bucket.blob(object_name)
        try:
            return blob.delete() is not None
        except Exception:
            pass

    def exists(self, object_name):
        """Checks whether object `object_name` exists

        Arguments:
            object_name {str} -- Name of object to check for existence

        Returns:
            bool -- flag for existence
        """

        return self.bucket.blob(object_name).exists()

    def metadata(self, object_name):
        """[summary]

        Arguments:
            object_name Name of object to get metadata for

        Raises:
            cpm.exceptions.NotFound -- If the object does not exist

        Returns:
            cpm.repository.ObjectMetadata -- The object Metadata
        """

        if not self.bucket.blob(object_name).exists():
            raise NotFound("{0} does not exist".format(object_name))
        blob = self.bucket.get_blob(object_name)
        return ObjectMetadata(blob.content_type, blob.md5_hash, blob.time_created)

    def list(self, prefix=""):
        """Lists all the objects in the bucket with prefix `prefix`

        Keyword Arguments:
            prefix {str} -- The prefix to use for the search (default: {""})

        Returns:
            list -- List of objects matching the search
        """

        return [o.name for o in self.bucket.list_blobs(prefix=prefix)]
