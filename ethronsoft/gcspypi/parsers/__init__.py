from .backup import BackupParser
from .syntax import SyntaxParser
from .download import DownloadParser
from .install import InstallParser
from .list import ListParser
from .remove import RemoveParser
from .search import SearchParser
from .syntax import SyntaxParser
from .uninstall import UninstallParser
from .upload import UploadParser

ALL_PARSERS = [
    BackupParser,
    SyntaxParser,
    DownloadParser,
    InstallParser,
    ListParser,
    RemoveParser,
    SearchParser,
    SyntaxParser,
    UninstallParser,
    UploadParser
]