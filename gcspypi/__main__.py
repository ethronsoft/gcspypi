import argparse
import os
import pm
import pb
import formatter


def main(args):
    pkg_mgr = pm.PackageManager(args["repository"], args["overwrite"])
    if args["search"]:
        pkgs = pb.PackageParser(args["search"]).parse()
        found = pkg_mgr.search(pkgs)
    elif args["remove"]:
        pkgs = pb.PackageParser(args["remove"]).parse()
        for pkg in pkgs:
            pkg_mgr.remove(pkg)
    elif args["upload"]:
        pkg = pb.PackageBuilder(args["upload"]).build()
        pkg_mgr.upload(pkg, args["overwrite"])
    elif args["install"]:
        pkgs = pb.PackageParser(args["install"]).parse()
        for pkg in pkgs:
            pkg_mgr.install(pkg)
        pass
    elif args["uninstall"]:
        pkgs = pb.PackageParser(args["uninstall"]).parse()
        for pkg in pkgs:
            pkg_mgr.uninstall(pkg)
        pass

        # class DistAction(argparse.Action):
        # def __call__(self, parser, namespace, values, option_string=None):
        # if getattr(namespace,"build") != None:
        # parser.error('Using dist after specifying --build is not allowed')
        # else:
        # setattr(namespace,"dist",values)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI to [G]oogle[C]loud[S]torage [PyPI]")
    parser.add_argument("-up", "--upload", metavar="FILE", type=str,
                        help="""Upload a package built by setup.py
				as either source, egg or wheel""")
    parser.add_argument("-o", "--overwrite", nargs="?", const=True, default=False, type=bool,
                        help="""Overwrites an existing package if
				user has delete permission on the 
				GCS repository""")
    parser.add_argument("-i", "--install", metavar="DEP", type=str,
                        help="""Downloads a package from the GCS
				repository and installs it locally
				via pip""")
    parser.add_argument("-m", "--mirror", nargs="?", const=True, default=False, type=bool,
                        help="""If package to install is not found
				in the GCS repository, attempts to
				use pip install, using the global configuration""")
    parser.add_argument("-u", "--uninstall", metavar="DEP", type=str,
                        help="""Uninstall a local package using pip
				uninstall""")
    parser.add_argument("-r", "--repository", metavar="R", type=str,
                        help="""Specifies GCS bucket name hosting
				the packages""")
    parser.add_argument("-s", "--search", metavar="QUERY", type=str,
                        help="""Searches for packages in the GCS repository
				matching the provided QUERY""")
    parser.add_argument("-rm", "--remove", metavar="QUERY", type=str,
                        help="""Removes packages from the GCS matching the
				provided QUERY if user has delete permission
				on the GCS repository. WARNING: Once executed,
				this cannot be undone if not by reinstalling
				the packages""")

    main(vars(parser.parse_args()))
