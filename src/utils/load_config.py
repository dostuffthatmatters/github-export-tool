import json
import os

d = os.path.dirname
PROJECT_DIR = d(d(d(os.path.abspath(__file__))))
OUT_DIR = os.path.join(PROJECT_DIR, "out")
META_FILE_PATH = os.path.join(PROJECT_DIR, "out", "github-meta.json")

if not os.path.exists(OUT_DIR):
    os.mkdir(OUT_DIR)

if not os.path.exists(META_FILE_PATH):
    with open(META_FILE_PATH, "w") as f:
        json.dump({}, f)


def load_config() -> tuple[list[str], list[str]]:
    try:
        with open(os.path.join(PROJECT_DIR, "config.json")) as f:
            config = json.load(f)
        assert isinstance(config, dict)
        assert "organizations" in config
        assert "exclude" in config
        organizations: list[str] = config["organizations"]
        excluded_repositories: list[str] = config["exclude"]
        assert isinstance(organizations, list)
        assert isinstance(excluded_repositories, list)
        assert all([isinstance(o, str) for o in organizations])
        assert all([isinstance(o, str) for o in excluded_repositories])
    except FileNotFoundError:
        raise FileNotFoundError("config.json does not exist")
    except Exception:
        raise Exception("config.json not in a valid format")

    return organizations, excluded_repositories
