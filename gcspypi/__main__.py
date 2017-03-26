import argparse
import os
import pm
import pb
import formatter


def print_syntax():
    print """
Syntax:
    (\w*)(==|=?<|=?>)?((?:\d*\.?){0,3})?,?(==|=?<|=?>)?((?:\d*\.?){0,3})?

Example:
    1) Refer to package 'abc' with version == 1.0.0
            abc==1.0.0
    2) Refer to package 'abc' with version  > 1.0.0
            abc>1.0.0
    3) Refer to package 'abc' with version <= 1.0.0
            abc<=1.0.0
    4) Refer to package 'abc' with version within a range.
       Selects the first match from the range lower bound
            abc>1.0.0,<=1.1.0
    5) Refer to latest version of all packages
            [no-args]
    6) Refer to every version of all packages
            >0.0.0

Note: a 0 may be omitted in specifying the version if followed by zeros
    i.e.
        *> would be equivalent to *>0.0.0
        1 would be equivalent to 1.0.0
        1.1 would be equivalent to 1.1.0
"""


def main(args):
    # pkg_mgr = pm.PackageManager(args["repository"], args["overwrite"], args["mirror"], not args["no_dependencies"])
    if args["command"] == "search":
        # pkgs = pkg_mgr.search(args["search"])
        pass
    elif args["command"] == "remove":
        # pkgs = pkg_mgr.search(args["remove"])
        # for pkg in pkgs:
        #    pkg_mgr.remove(pkg)
        pass
    elif args["command"] == "upload":
        # pkg = pb.PackageBuilder(args["upload"]).build()
        # pkg_mgr.upload(pkg, args["overwrite"])
        pass
    elif args["command"] == "install":
        # for name in args["install"]:
        #    pkg_mgr.install(pb.Package.from_text(name))
        pass
    elif args["command"] == "uninstall":
        # pkgs = pb.PackageParser(args["uninstall"]).parse()
        # for name in args["uninstall"]:
        #    pkg_mgr.uninistall(pb.Package.from_text(name))
        pass
    elif args["command"] == "syntax":
        print_syntax()
    elif args["command"] == "pull":
        pass
    elif args["command"] == "push":
        pass
    else:
        # help find missing elif clauses if new commands are added
        raise Exception("Unrecognized command")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CLI to [G]oogle [C]loud [S]torage [PyPI]")
    parser.add_argument("--repository", metavar="R", type=str,
                        help="Specifies GCS bucket name hosting the packages")
    subparsers = parser.add_subparsers(title="commands", help="use command --help for help", dest="command")
    # upload
    updload_parser = subparsers.add_parser("upload",
                                           description="Upload a package built by setup.py as either source, egg or wheel")
    updload_parser.add_argument("file", metavar="FILE", type=str, help="Package to upload")
    updload_parser.add_argument("-o", "--overwrite", nargs="?", const=True, default=False, type=bool,
                                help="Overwrites an existing package if user has delete permission on the GCS repository")
    # install
    install_parser = subparsers.add_parser("install",
                                           description="""Downloads a package from the GCS repository,
                                      (or pypi index if mirroring is enabled) and installs it locally""")
    install_parser.add_argument("packages", metavar="P", nargs="*", type=str, help="Package(s) to install. View syntax using command syntax")
    install_parser.add_argument("-r", "--requirements", metavar="F", nargs="?", type=str,
                                help="Additional requirements to install")
    install_parser.add_argument("-m", "--mirror", nargs="?", const=True, default=False, type=bool,
                                help="""If package to install is not found
                                                in the GCS repository, attempts to
                                                use pip install, using the global configuration""")
    install_parser.add_argument("-nd", "--no-dependencies", nargs="?", const=True, default=False, type=bool,
                                help="""Omit downloading package dependencies""")
    # uninstall
    uninstall_parser = subparsers.add_parser("uninstall", description="Uninstall a local package")
    uninstall_parser.add_argument("packages", metavar="P", nargs="*", type=str, help="Package(s) to uninstall")
    # search
    seach_parser = subparsers.add_parser("search",
                                         description="Search for packages in the GCS repository. View syntax using command syntax")
    # remove
    remove_parser = subparsers.add_parser("remove",
                                          description="""Removes packages from the GCS if user has delete permission
                                                        on the GCS repository. WARNING: Once executed,
                                                        this command cannot be undone if not by reinstalling
                                                        the packages. View syntax using command syntax""")
    # backup
    pull_parser = subparsers.add_parser("pull", description="Pulls the repository at the provided location")
    pull_parser.add_argument("destination", default=".", help="Directory to pull into")
    push_parser = subparsers.add_parser("push", description="Pushes the local copy of the repository to the repository")
    push_parser.add_argument("destination", help="Repository to push into")
    # syntax-example
    syntax_parser = subparsers.add_parser("syntax", description="Describes syntax used in search and remove commands")

    args = vars(parser.parse_args())
    print args
    main(args)
