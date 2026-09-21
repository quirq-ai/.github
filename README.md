# Quirq on GitHub

The public organization profile and shared community guidelines for [quirq-ai](https://github.com/quirq-ai).

**Looking for the product?** [Run XO Space locally](https://github.com/quirq-ai/xo-space#quick-start), [open the hosted app](https://app.xo.builders/), or [read the documentation](https://docs.xo.builders/).

## What lives here

| Path | Purpose |
| --- | --- |
| [profile/README.md](profile/README.md) | The public organization overview. |
| [profile/assets/](profile/assets/) | Repository-owned profile artwork and its provenance. |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute across Quirq repositories. |
| [SUPPORT.md](SUPPORT.md) | Where to ask questions, report bugs and get account help. |
| [SECURITY.md](SECURITY.md) | Private security-reporting guidance. |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community expectations and reporting. |
| [.github/ISSUE_TEMPLATE/](.github/ISSUE_TEMPLATE/) | Default bug and feature forms and help links. |
| [.github/PULL_REQUEST_TEMPLATE.md](.github/PULL_REQUEST_TEMPLATE.md) | A short problem, change and validation template. |
| [docs/maintaining.md](docs/maintaining.md) | Profile decisions, inheritance rules and the maintenance checklist. |

## How defaults work

GitHub uses supported files in this public `.github` repository when a Quirq repository does not supply its own. Repository-specific guidance takes precedence. A repository with its own valid issue templates or issue-template configuration replaces the **entire** inherited template directory; GitHub does not merge them.

These files are not copied into product checkouts. Workflows and `CODEOWNERS` are not organization-wide defaults, and licenses remain the responsibility of each repository. See [GitHub's community-file documentation](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).

## Check a change

Use Python 3.12 or newer:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
```

The check validates local Markdown links, profile assets and GitHub configuration. Public destination checks and visual review are separate: follow the [maintenance checklist](docs/maintaining.md#before-merging).

Open pull requests against **main**. Changes become the organization profile and eligible repository defaults when merged. XO Space has its own [contribution workflow](https://github.com/quirq-ai/xo-space/blob/main/CONTRIBUTING.md), including a different target branch.
