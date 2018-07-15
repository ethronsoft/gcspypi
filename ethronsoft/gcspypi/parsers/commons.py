from ethronsoft.gcspypi.repository.gcloud_remote import GCloudRepository
from ethronsoft.gcspypi.exceptions import InvalidParameter
import os

def init_repository(console, repository):
    if not repository:
        raise InvalidParameter("missing repository. Use --repository flag or write entry repository=<repo_name> in ~/.gcspypirc")
    try:
        console.info("using repository {}".format(repository))
        pending = console.badge("connecting...", "warning", overwrite=True)
        repo = GCloudRepository(repository)
        console.blank(pending)
        console.badge("connected", "success")
        return repo
    except:
        console.blank(pending)
        console.badge("failed connecting", "danger")
        raise
