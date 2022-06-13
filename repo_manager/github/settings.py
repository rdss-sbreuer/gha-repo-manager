from collections.abc import Callable
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union

from github.Repository import Repository

from repo_manager.schemas.settings import Settings


def check_repo_settings(repo: Repository, settings: Settings) -> Tuple[bool, List[Optional[str]]]:
    """Checks a repo's settings vs our expected settings

    Args:
        repo (Repository): [description]
        settings (Settings): [description]

    Returns:
        Tuple[bool, Optional[List[str]]]: [description]
    """

    def get_repo_value(setting_name: str, repo: Repository) -> Optional[Any]:
        """Get a value from the repo object"""
        getter_val = SETTINGS[setting_name].get("get", setting_name)
        if getter_val is None:
            return None
        getter = getattr(repo, getter_val)
        if not callable(getter):
            return getter
        else:
            return getter()

    drift = []
    checked = True
    for setting_name in settings.dict().keys():
        repo_value = get_repo_value(setting_name, repo)
        if repo_value is None:
            continue
        settings_value = getattr(settings, setting_name)
        if repo_value != settings_value:
            drift.append(f"{setting_name} -- Expected: '{settings_value}' Found: '{repo_value}'")
            checked = False
    return checked, drift


def update(repo: Repository, setting_name: str, new_value: Any):
    """[summary]

    Args:
        repo (Repository): [description]
        setting_name (str): [description]
        new_value (Any): [description]
    """
    ...


def set_topics(repo: Repository, setting_name: str, new_value: Any):
    """[summary]

    Args:
        repo (Repository): [description]
        setting_name (str): [description]
        new_value (Any): [description]
    """
    ...


def set_security_fixes(repo: Repository, setting_name: str, new_value: Any):
    """[summary]

    Args:
        repo (Repository): [description]
        setting_name (str): [description]
        new_value (Any): [description]
    """
    ...


def set_vuln_alerts(repo: Repository, setting_name: str, new_value: Any):
    """[summary]

    Args:
        repo (Repository): [description]
        setting_name (str): [description]
        new_value (Any): [description]
    """
    ...


# "name_of_setting_from_repo_manager.schemas.settings.Settings": {
#   Optional entry, a method to call on the repo object to get a setting.
#   Default is the name of the setting
#   If the value of repo.getatter(get) is a callable, we'll call it to get the result
#   "get": "get_setting"
#   Optional entry, a method to call to update this setting on the repo. Is passed the repo, setting_name, and new_value
#   Default is repo_manager.github.settings.update
# }
# an empty dict means to just use the default methods
SETTINGS = {
    "description": {},
    "homepage": {},
    "topics": {"get": "get_topics", "set": set_topics},
    "private": {},
    "has_issues": {},
    "has_projects": {},
    "has_wiki": {},
    "has_downloads": {},
    "default_branch": {},
    "allow_squash_merge": {},
    "allow_merge_commit": {},
    "allow_rebase_merge": {},
    "delete_branch_on_merge": {"set": ""},
    # Checks set to none are for values that there are no api endpoints to get
    # Like the security and vulnerability alerts
    "enable_automated_security_fixes": {"get": None, "set": set_security_fixes},
    "enable_vulnerability_alerts": {"get": None, "set": set_vuln_alerts},
}
