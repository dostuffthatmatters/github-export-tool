import json
import os
from typing import Optional
from .run_shell_command import run_shell_command

d = os.path.dirname
PROJECT_DIR = d(d(d(os.path.abspath(__file__))))
OUT_DIR = os.path.join(PROJECT_DIR, "out")
META_FILE_PATH = os.path.join(PROJECT_DIR, "out", "github-meta.json")


def get_last_update_time_from_github(
    organization: str, repository: str, github_cli: str
) -> str:
    return json.loads(
        run_shell_command(
            f"{github_cli} repo view {organization}/{repository} --json pushedAt"
        )
    )["pushedAt"]


def get_last_update_time_from_cache(
    organization: str, repository: str
) -> Optional[str]:
    with open(META_FILE_PATH, "r") as f:
        github_meta = json.load(f)
    try:
        return github_meta[f"{organization}/{repository}"]
    except KeyError:
        return None


def write_update_time_to_cache(
    organization: str, repository: str, last_update_time: str
) -> None:
    with open(META_FILE_PATH, "r") as f:
        github_meta = json.load(f)
    github_meta[f"{organization}/{repository}"] = last_update_time
    with open(META_FILE_PATH, "w") as f:
        json.dump(github_meta, f, indent=4)
