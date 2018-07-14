class SyntaxParser(object):

    def __init__(self, subparsers):
        self.name = "syntax"
        subparsers.add_parser(self.name, description="Describes syntax used in search and remove commands")

    def handle(self, config, data):
        pass