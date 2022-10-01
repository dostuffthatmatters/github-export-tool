import json
import os
import shutil
from .run_shell_command import run_shell_command

d = os.path.dirname
PROJECT_DIR = d(d(d(os.path.abspath(__file__))))
OUT_DIR = os.path.join(PROJECT_DIR, "out")


def get_organization_repositories(organization: str, github_cli: str) -> list[str]:
    stdout = run_shell_command(
        f"{github_cli} repo list {organization} --json name --limit 1000"
    )
    return [x["name"] for x in json.loads(stdout)]


def download_repository(organization: str, repository: str) -> None:
    repo_dir = os.path.join(OUT_DIR, organization, repository)
    code_dir = os.path.join(repo_dir, "code")
    if os.path.exists(repo_dir):
        shutil.rmtree(repo_dir)
    run_shell_command(f"mkdir -p {repo_dir}")

    run_shell_command(
        f"git clone git@github.com:{organization}/{repository}.git --mirror "
        + os.path.join(code_dir, ".git")
    )
    run_shell_command("git config --bool core.bare false", cwd=code_dir)
    run_shell_command("git reset --hard", cwd=code_dir)

    # TODO: download issues
    # TODO: download pull requests
    # TODO: download releases
    # TODO: download LFS items


def get_downloaded_size(organization: str, repository: str) -> str:
    repo_dir = os.path.join(OUT_DIR, organization, repository)
    p = run_shell_command(f"du -d 0 -h {repo_dir}")
    return p.replace("\t", " ").split(" ")[0]
