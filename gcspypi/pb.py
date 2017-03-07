
class Package(object):
	def __init__(self, name, version, namespace = ""):
		self.__name = name
		self.__version = self.__checked_version(version)
		self.__namespace = namespace
		
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
				
	@property
	def namespace(self):
		return self.__name
		
class SourcePackage(Package):
	def __init__(self, source_dir):	
		self.__source_dir = source_dir
		
	def prepare(self):
		Package.prepare(self)
		
	def __extract_source_info(self):
		pass
		
class BinPackage(Package):
	def __init__(self, source_dir, bin_type):	
		self.__source_dir = source_dir
		self.__bin_type = bin_type
		
	def prepare(self):
		Package.prepare(self)
		
	def __extract_source_info(self):
		pass		
		
class PackageBuilder(object):
	def __init__(self, args):
		self.__args = args	
	
	def build(self):
		return Package("some","1.0.0","namespace")