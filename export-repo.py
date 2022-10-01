import json
import os
import shutil
import subprocess
from typing import Optional

ORGANIZATIONS = ["tum-esm"]
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(PROJECT_DIR, "out")


def run_shell_command(command: str, cwd: Optional[str] = None) -> str:
    process = subprocess.run(command.split(" "), capture_output=True, cwd=cwd)
    assert process.returncode == 0, f'command "{command}" failed'
    return process.stdout.decode()


def get_organization_repositories(organization: str) -> list[str]:
    stdout = run_shell_command(f"gh repo list {organization} --json name --limit 1000")
    return [x["name"] for x in json.loads(stdout)]


if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.mkdir(OUT_DIR)

for organization in ORGANIZATIONS:
    assert " " not in organization, "spaces not allowed in organization names"

    repositories = get_organization_repositories(organization)

    if not os.path.exists(os.path.join(OUT_DIR, organization)):
        shutil.rmtree(OUT_DIR)
    os.mkdir(OUT_DIR)

    for repository in repositories:
        assert " " not in repository, "spaces not allowed in repository names"
