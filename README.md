# 💾 &nbsp;Github Export Tool

A tool that downloads everything from a list of github organizations and users.

-   [x] ⚙️ &nbsp;Code (with all branches and tags)
-   [ ] 🪲 &nbsp;Issues
-   [ ] ⚔️ &nbsp;Pull Requests
-   [ ] 📍 &nbsp;Releases
-   [ ] 🚛 &nbsp;LFS items

This can be used to periodically backup your whole organization. Existing tools that do this backup are crazy expensive (like https://rewind.com/pricing-backups/). And export via a migration is only available for GitHub enterprise.

Under the hood, this tool uses the [GitHub CLI](https://cli.github.com/). Only works when using authentication via SSH. If you want HTTPS support 👉 PRs are welcome.
