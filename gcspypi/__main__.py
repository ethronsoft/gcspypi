import argparse
import os
import pm
import pb
import formatter

def main(args):
	pkg_mgr = pm.PackageManager(args["repository"])
	if args["list"]:
		pkg_mgr.list(args["list"])
	elif args["remove"]:
		pkg = pb.Package("some","1.0.0","namespace")
		pkg_mgr.remove(pkg)
	elif args["build"] or args["dist"]:
		builder = pb.PackageBuilder(args)
		pkg = builder.build()
		pkg_mgr.upload(pkg,args["overwrite"])
		
	
class BuildAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if getattr(namespace,"build_dir") == None:
			parser.error('Missing parameter --build-dir')
		elif getattr(namespace,"dist") != None:
			parser.error('Using build after specifying --dist is not allowed')
		else:
			setattr(namespace,"build",values)
			
			
class DistAction(argparse.Action):
	def __call__(self, parser, namespace, values, option_string=None):
		if getattr(namespace,"build") != None:
			parser.error('Using dist after specifying --build is not allowed')
		else:
			setattr(namespace,"dist",values)
			
	
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Some description")
	parser.add_argument("-d","--dist",metavar="D", type=str, action=DistAction, help="Some Help")
	parser.add_argument("-b","--build",metavar="B", choices=["source","wheel","egg"], action=BuildAction,help="Some Help")
	parser.add_argument("-bd","--build-dir",metavar="BD", default=".", type=str, help="Some Help")
	parser.add_argument("-o","--overwrite",metavar="O", nargs="?", default=False, type=bool, help ="Some Help")
	parser.add_argument("-r","--repository",metavar="R", required=True, type=str, help="Some Help")
	parser.add_argument("-ls","--list",metavar="PREFIX", type=str, help="Some Help")
	parser.add_argument("-rm","--remove",metavar="PREFIX", type=str, help="Some Help")
	
	main(vars(parser.parse_args()))