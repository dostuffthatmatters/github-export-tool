# 💾 &nbsp;Github Export Tool

A tool that downloads everything from a list of GitHub organizations and users.

-   [x] ⚙️ &nbsp;Code (with all branches and tags)
-   [ ] 🪲 &nbsp;Issues
-   [ ] ⚔️ &nbsp;Pull Requests
-   [ ] 📍 &nbsp;Releases
-   [ ] 🚛 &nbsp;LFS items

This can be used to periodically back up your whole organization. Existing tools that do this backup are crazy expensive (like https://rewind.com/pricing-backups/). And export via migration is only available for GitHub Enterprise.

Under the hood, this tool uses the [GitHub CLI](https://cli.github.com/).

*Only works when using authentication via SSH. If you want HTTPS support 👉 PRs are welcome.*

<br/>

## ⚔️ How to Use it?

1. Install Poetry (https://python-poetry.org/)
2. Install Python3.10 (https://python.org/)
3. Install the GitHub CLI (https://cli.github.com/)
4. Authenticate your GitHub CLI

```bash
gh auth
```

5. Create venv and install dependencies:

```bash
python3.10 -m venv .venv
source .venv/bin/activate
poetry install
```

6. Use the `config.default.json` to create a `config.json`
7. Run

```bash
python run.py
```

<br/>

## 🥷 Some Details

For each organization, it calls `gh repo list <org> --json name --limit 1000` to get the respective repository names.

It clones the repo with all branches using `git clone git@github.com:<org>/<repo>.git --mirror`.

It only downloads the repositories that have been updates since the last run. Using the `gh repo view <org>/<repo> --json pushedAt` command for every repo, it fetches the last commit time on any branch.


