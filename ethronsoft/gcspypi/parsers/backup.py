
class BackupParser(object):

    def __init__(self, subparsers):
        self.name = "backup"
        backup_parser = subparsers.add_parser(self.name, description="Allows to backup and restore a repository")
        backup_subparser = backup_parser.add_subparsers(title="backup commands", help="use command --help for help", dest="sub_command")
        pull_parser = backup_subparser.add_parser("pull", description="Pulls the repository at the provided location")
        pull_parser.add_argument("destination", default=".", help="Directory to pull into")
        push_parser = backup_subparser.add_parser("push", description="Pushes the local copy of the repository to the repository")
        push_parser.add_argument("zipped_repo", help="Name o zipped repository to push")

    def handle(self, config, data):
        pass