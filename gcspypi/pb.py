import zipfile
import shutil
import os
import glob
import json
import yaml

class Package(object):
	def __init__(self, name, version):
		self.__name = name
		self.__version = self.__checked_version(version)
		
	def __checked_version(self,v):
		if (len(v.split(".")) != 3): raise Exception("Version must be provided in major.minor.patch format")
		return v
		
	def __del__(self):
		print "Package destructor"
		
	def prepare(self):
		return "some"
		
	@property
	def name(self):
		return self.__name
				
	@property
	def version(self):
		return self.__name

class PackageParser(object):
	def __init__(self, syntax):
		pass
	
		
	def parse(self):
		pass
		
class PackageBuilder(object):

	def __init__(self,raw_package):
		if 	(".zip" in raw_package or ".tar" in raw_package):
			self.__info = __extract_source(raw_package)
		elif(".egg" in raw_package):
			self.__info = __extract_egg(raw_package)
		elif(".whl" in raw_package):
			self.__info = __extract_wheel(raw_package)
		else:
			raise Exception("Unrecognized file extension. expected {.zip|.tar|.tar.gz|.egg|.whl}")	
			
	def __seek_and_apply(self, raw_package, target, command):
		try:
			cwd = os.getcwd()
			dir = tempfile.mkdtemp()
			os.chdir(dir)
			with zipfile.ZipFile(raw_package,"r") as f:
				f.extractall(".")
				with root,dir,file in os.walk("."):
					if file == target:
						with open(os.path.join(root,file),"r") as target_file:
							command(target_file)
						break
		finally:
			shutil.rmtree(dir)
			os.chdir(cwd)
			
	def __extract_egg(self,raw_package):
		#egg needs to get data from PKG-INFO, just like source...
		return self.__extract_source(raw_package)		
		
	def __extract_source(self,raw_package):
		class Apply(object):
			def __init__(self):
				self.metadata = {}
			def __call__(self, target):	
				map = {}
				for line in target.readlines():
					k,v = line.split(":")
					map[k] = v
				metadata["name"] = map["name"]
				metadata["version"] = map["version"]
		apply = Apply()			
		self.__seek_and_apply(raw_package,"PKG-INFO",apply)
		if not apply.metadata:
			raise Exception("Could not find PKG-INFO in: " + raw_package)
		return 	apply.metadata
			
	def __extract_wheel(self,raw_package):
		class Apply(object):
			def __init__(self):
				self.metadata = {}
			def __call__(self, target):	
				map = json.loads(target,"r").read())
				metadata["name"]= map["name"]
				metadata["version"] = map["version"]
					
		apply = Apply()			
		self.__seek_and_apply(raw_package,"metadata.json",apply)
		if not apply.metadata:
			raise Exception("Could not find PKG-INFO in: " + raw_package)
		return 	apply.metadata
	
	def build(self):
		return Package(self.__info.name, self.__info.version)