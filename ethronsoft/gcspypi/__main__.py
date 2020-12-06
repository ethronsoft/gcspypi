from __future__ import print_function
from ethronsoft.gcspypi.parsers import ALL_PARSERS
import argparse
import os
from colorama import init


def main():
    parser = argparse.ArgumentParser(description="CLI to [G]oogle [C]loud [S]torage [PyPI]")
    parser.add_argument("--repository", metavar="R", type=str, nargs="?",
                        help="Specifies GCS bucket name hosting the packages. If not provided, gcspypi will try to read it from ~/.gcspypirc")
    parser.add_argument("--verbose", "-v", action="store_true", default=False,
                        help="Verbose mode: exceptions stacktraces will be printed")
    parser.add_argument("--python3", action="store_true", default=False,
                        help="Python3 mode: run in python3 mode")
    subparsers = parser.add_subparsers(title="commands", help="use command --help for help", dest="command")
    
    #init colorama
    init()

    #init parsers
    parsers = [p(subparsers) for p in ALL_PARSERS]
    #map handlers
    handlers = {
        p.name: p.handle for p in parsers
    }

    args = vars(parser.parse_args())
    # process(args)
    repository = args.get("repository")
    if not repository:
        #let's check in the ~/.gcspypirc
        rc = os.path.join(os.path.expanduser("~"), ".gcspypirc")
        if os.path.exists(rc):
            with open(rc, "r") as f:
                lines = [x.lower().strip() for x in  f.readlines()]
                reporc = [x for x in lines if x.startswith("repository")]
                if reporc and "=" in reporc[0]:
                    [_, value] = reporc[0].split("=")
                    repository = value.strip()
    config = {
        "repository": repository,
        "python3": args.get("python3")
    }
    handlers[args["command"]](config, args)

if __name__ == "__main__":
    main()
