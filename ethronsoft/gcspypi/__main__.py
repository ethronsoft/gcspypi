from __future__ import print_function
import argparse
import os

import pb
import pm


def print_syntax():
    print("""
Syntax:
    ((?:\w|-)*)(==|=?<|=?>)?((?:\d*\.?){0,3})?,?(==|=?<|=?>)?((?:\d*\.?){0,3})?

Example:
    1) Refer to package 'abc' with version == 1.0.0
            abc==1.0.0
    2) Refer to package 'abc' with version  > 1.0.0
            abc>1.0.0
    3) Refer to package 'abc' with version <= 1.0.0
            abc<=1.0.0
    4) Refer to package 'abc' with version within a range.
       Selects the first match from the range lower bound
            abc>1.0.0,<=1.2.0
    5) Refer to last version of package 'abc'
            abc
    6) Refer to last version of all packages
            [empty]
    7) Refer to every version of all packages
            >0.0.0

Note: a 0 may be omitted in specifying the version if followed by zeros
    i.e.
        > would be equivalent to >0.0.0
        1 would be equivalent to 1.0.0
        1.1 would be equivalent to 1.1.0
""")


def process(args):
    if args["command"] == "search":
        pkg_mgr = pm.PackageManager(args["repository"])
        for syntax in args["syntax"]:
            pkg = pkg_mgr.search(syntax)
            print(pkg)
    elif args["command"] == "list":
        pkg_mgr = pm.PackageManager(args["repository"])
        for path in sorted(pkg_mgr.list_items(args["package"], True)):
                print(path.split("/")[-1])
    elif args["command"] == "download":
        pkg_mgr = pm.PackageManager(args["repository"])
        print("Downloaded: {0}".format(pkg_mgr.download_by_name(args["obj"], args["dir"])))
    elif args["command"] == "remove":
        pkg_mgr = pm.PackageManager(args["repository"])
        for syntax in args["packages"]:
            pkg = pkg_mgr.search(syntax)
            ok = pkg is not None
            while ok:
                ok = pkg_mgr.remove(pkg)
    elif args["command"] == "upload":
        pkg_mgr = pm.PackageManager(args["repository"], overwrite=args["overwrite"])
        pkg = pb.PackageBuilder(os.path.abspath(args["file"])).build()
        pkg_mgr.upload(pkg, os.path.abspath(args["file"]))
    elif args["command"] == "install":
        pkg_mgr = pm.PackageManager(args["repository"],
                                    mirroring=args["mirror"], install_deps=not args["no_dependencies"])
        for syntax in args["packages"]:
            pkg_mgr.install(syntax, args["type"], args["no_user"])
    elif args["command"] == "uninstall":
        pkg_mgr = pm.PackageManager(args["repository"])
        for syntax in args["packages"]:
            pkg_mgr.uninstall(pb.Package.from_text(syntax))
    elif args["command"] == "syntax":
        print_syntax()
    elif args["command"] == "pull":
        pkg_mgr = pm.PackageManager(args["repository"])
        pkg_mgr.clone(args["destination"])
    elif args["command"] == "push":
        pkg_mgr = pm.PackageManager(args["repository"])
        pkg_mgr.restore(args["zipped_repo"])
    else:
        # help find missing elif clauses if new commands are added
        raise Exception("Unrecognized command")


def main():
    parser = argparse.ArgumentParser(description="CLI to [G]oogle [C]loud [S]torage [PyPI]")
    parser.add_argument("--repository", metavar="R", type=str, nargs="?",
                        help="Specifies GCS bucket name hosting the packages")
    subparsers = parser.add_subparsers(title="commands", help="use command --help for help", dest="command")
    # upload
    updload_parser = subparsers.add_parser("upload",
                                           description="Upload a package built by setup.py as either source or wheel")
    updload_parser.add_argument("file", metavar="FILE", type=str, help="Package to upload")
    updload_parser.add_argument("-o", "--overwrite", nargs="?", const=True, default=False, type=bool,
                                help="Overwrites an existing package if user has delete permission on the GCS repository")

    # download
    download_parser = subparsers.add_parser("download",
                                           description="Download a package by the provided name")
    download_parser.add_argument("obj", metavar="FILE", type=str, help="Package to download")
    download_parser.add_argument("dir", default=".", type=str,
                                help="directory where to download the file")

    # install
    install_parser = subparsers.add_parser("install",
                                           description="""Downloads a package from the GCS repository,
                                      (or pypi index if mirroring is enabled) and installs it locally""")
    install_parser.add_argument("packages", metavar="P", nargs="*", type=str,
                                help="Package(s) to install. View syntax using command syntax")
    install_parser.add_argument("-r", "--requirements", metavar="F", nargs="?", type=str,
                                help="Additional requirements to install")
    install_parser.add_argument("-m", "--mirror", nargs="?", default=True, type=bool,
                                help="""If package to install is not found
                                                in the GCS repository, attempts to
                                                use pip install, using the global configuration""")
    install_parser.add_argument("-nd", "--no-dependencies", nargs="?", default=False, type=bool,
                                help="""Omit downloading package dependencies""")
    install_parser.add_argument("-t", "--type", nargs="?", default="SOURCE", choices=['SOURCE', 'WHEEL'])
    install_parser.add_argument("--no-user", default=False, const=True, nargs="?", type=bool, help="do not use option --user when installing a package via `pip install`")
    # uninstall
    uninstall_parser = subparsers.add_parser("uninstall", description="Uninstall a local package")
    uninstall_parser.add_argument("packages", metavar="P", nargs="*", type=str, help="Package(s) to uninstall")
    # search
    seach_parser = subparsers.add_parser("search",
                                         description="Search for packages in the GCS repository. View syntax using command syntax")
    seach_parser.add_argument("syntax", nargs="+", help="Search syntax")
    # list
    list_parser = subparsers.add_parser("list",
                                        description="""Displays all versions of a certain package
                                        or all content of the repository if package name is omitted""")
    list_parser.add_argument("package", nargs="?", default="", help="Package Name")
    # remove
    remove_parser = subparsers.add_parser("remove",
                                          description="""Removes packages from the GCS if user has delete permission
                                                        on the GCS repository. WARNING: Once executed,
                                                        this command cannot be undone if not by reinstalling
                                                        the packages. View syntax using command syntax""")
    remove_parser.add_argument("packages", metavar="P", nargs="+", type=str,
                               help="Package(s) to remove. View syntax using command syntax")
    # backup
    pull_parser = subparsers.add_parser("pull", description="Pulls the repository at the provided location")
    pull_parser.add_argument("destination", default=".", help="Directory to pull into")
    push_parser = subparsers.add_parser("push", description="Pushes the local copy of the repository to the repository")
    push_parser.add_argument("zipped_repo", help="Name o zipped repository to push")
    # syntax-example
    syntax_parser = subparsers.add_parser("syntax", description="Describes syntax used in search and remove commands")

    args = vars(parser.parse_args())
    process(args)

if __name__ == "__main__":
    main()
