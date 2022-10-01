import os
from src import utils
import rich.progress

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR = os.path.join(PROJECT_DIR, "out")


def run() -> None:
    organizations, excluded_repositories = utils.load_config()
    repositories = {o: utils.get_organization_repositories(o) for o in organizations}
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
                if f"{o}/{r}" in excluded_repositories:
                    progress.console.print(f"Skipping {o}/{r}")
                    progress.update(task, advance=1)
                else:
                    progress.console.print(f"Processing {o}/{r}")
                    last_github_update_time = utils.get_last_update_time_from_github(
                        o, r
                    )
                    last_cache_update_time = utils.get_last_update_time_from_cache(o, r)
                    repo_path = os.path.join(OUT_DIR, o, r, "code", ".git")

                    if (last_github_update_time != last_cache_update_time) or (
                        not os.path.isdir(repo_path)
                    ):
                        utils.write_update_time_to_cache(o, r, last_github_update_time)
                        utils.download_repository(o, r)
                        size = utils.get_downloaded_size(o, r)
                        progress.console.print(
                            f"✅ Done. Total downloaded size is {size}"
                        )
                    else:
                        progress.console.print(f"✅ Done. Already up-to-date")
                    progress.update(task, advance=1)
