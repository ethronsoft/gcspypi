from google.cloud import storage
from pb import Package

class PackageManager(object):
	
	def __init__(self, repo_name):
		self.__bucket_name = repo_name
		pass
		
	def __get_bucket(self):
		pass
		###return a client using the current default login 
		###set with: gcloud auth application-default login
		#return storage.Client().bucket(self.__bucket_name)
		
	def upload(self, pkg, overwrite):
		print "uploading"
		pass
		#repo_object_name = "some"
		#blob = self.__get_bucket.blob(repo_object_name)
		#blob.upload_from_filename(filename)
		
	def download(self, pkg):
		print "downloading"
		pass
		#target_file_name = "some.in"
		#output_file_name = "some.out"
		#blob = self.__get_bucket.blob(repo_object_name)
		#blob.download_to_filename(output_file_name)	
		
	def list(self, prefix):
		print "listing"
		pass
		#list_res = self.__get_bucket.list_blobs(prefix=prefix)
		##let's return ordered, for searching and visual reasons
		#def comp(i, x):
		#	if   (i.name == x.name): return 0
		#	elif (i.name <  x.name): return -1
		#	else				      : return 1
		#return sorted(list_res,cmp=comp)
	
	def remove(self, pkg):
		print "removing"
		pass