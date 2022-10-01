import json
import os
import shutil
import subprocess
from typing import Optional
import rich.progress

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(PROJECT_DIR, "out")

try:
    with open(os.path.join(PROJECT_DIR, "config.json")) as f:
        config = json.load(f)
    assert isinstance(config, dict)
    assert "organizations" in config
    organizations = config["organizations"]
    assert isinstance(organizations, list)
    assert all([isinstance(o, str) for o in organizations])
except FileNotFoundError:
    raise FileNotFoundError("config.json does not exist")
except Exception:
    raise Exception("config.json not in a valid format")


def run_shell_command(command: str, cwd: Optional[str] = None) -> str:
    process = subprocess.run(command.split(" "), capture_output=True, cwd=cwd)
    assert process.returncode == 0, f'command "{command}" failed'
    return process.stdout.decode().strip()


def get_organization_repositories(organization: str) -> list[str]:
    stdout = run_shell_command(f"gh repo list {organization} --json name --limit 1000")
    return [x["name"] for x in json.loads(stdout)]


def download_repository(organization: str, repository: str) -> None:
    repo_dir = os.path.join(OUT_DIR, organization, repository)
    code_dir = os.path.join(repo_dir, "code")
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


if os.path.exists(OUT_DIR):
    shutil.rmtree(OUT_DIR)
os.mkdir(OUT_DIR)

repositories = {o: get_organization_repositories(o) for o in organizations}
repository_count = sum([len(repositories[o]) for o in organizations])
for o in organizations:
    assert " " not in o, "spaces not allowed in organization names"
    for r in repositories[o]:
        assert " " not in r, "spaces not allowed in repository names"

with rich.progress.Progress() as progress:
    task = progress.add_task(
        "Downloading GitHub Repositories",
        total=repository_count,
    )

    for o in organizations:
        for r in repositories[o]:
            progress.console.print(f"Processing {o}/{r}")
            download_repository(o, r)
            size = get_downloaded_size(o, r)
            progress.console.print(f"✅ Done. Total size is {size}")
            progress.update(task, advance=1)
