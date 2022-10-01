import os
from src import utils
import rich.progress

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(PROJECT_DIR, "out")


def run() -> None:
    organizations, excluded_repositories, github_cli = utils.load_config()
    repositories = {
        o: utils.get_organization_repositories(o, github_cli) for o in organizations
    }
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

        iteration = 0
        for o in organizations:
            for r in repositories[o]:
                iteration += 1
                if f"{o}/{r}" in excluded_repositories:
                    progress.console.print(
                        f"({iteration}/{repository_count}) Skipping {o}/{r}", end="\n\n"
                    )
                    progress.update(task, advance=1)
                else:
                    progress.console.print(
                        f"({iteration}/{repository_count}) Processing {o}/{r}"
                    )
                    last_github_update_time = utils.get_last_update_time_from_github(
                        o, r, github_cli
                    )
                    last_cache_update_time = utils.get_last_update_time_from_cache(o, r)
                    repo_path = os.path.join(OUT_DIR, o, r, "code", ".git")

                    if (last_github_update_time != last_cache_update_time) or (
                        not os.path.isdir(repo_path)
                    ):
                        progress.console.print(f"🐘 New download necessary")
                        utils.download_repository(o, r)
                        utils.write_update_time_to_cache(o, r, last_github_update_time)
                    else:
                        progress.console.print(f"🕊 Already up-to-date")
                    size = utils.get_downloaded_size(o, r)
                    progress.console.print(f"✅ Done. Total size is {size}", end="\n\n")
                    progress.update(task, advance=1)
