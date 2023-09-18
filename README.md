# 💾 &nbsp;Github Export Tool

A tool that downloads everything from a list of GitHub organizations and users.

- [x] ⚙️ &nbsp;Code (with all branches and tags)
- [ ] 🪲 &nbsp;Issues
- [ ] ⚔️ &nbsp;Pull Requests
- [ ] 📍 &nbsp;Releases
- [ ] 🚛 &nbsp;LFS items

This can be used to periodically back up your whole organization. Existing tools that do this backup are crazy expensive (like https://rewind.com/pricing-backups/). And export via migration is only available for GitHub Enterprise.

Under the hood, this tool uses the [GitHub CLI](https://cli.github.com/). Currently only works when using authentication via SSH.

**🙌 Contributions are welcome.**

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

6. Use the `config.template.json` to create a `config.json`
7. Run

```bash
python run.py
```

<br/>

## 🥷 Some Details

- For each organization/username, it calls `gh repo list <org-or-user> --json name --limit 1000` to get the respective repository names.
- It clones the repo with all branches using `git clone git@github.com:<org-or-user>/<repo>.git --mirror`.
- It only downloads the repositories that have been updated since the last run. Using the `gh repo view <org-or-user>/<repo> --json pushedAt` command for every repo, it fetches the last commit time on any branch and saves it to `out/github-meta.json`.
- You can configure the command used to call the GitHub CLI. Since the abbreviation `gh` is very short you could just set the actual path - e.g. `config.github_cli = "/opt/homebrew/bin/gh"`.
