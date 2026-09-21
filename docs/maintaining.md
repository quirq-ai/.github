# Maintaining the Quirq GitHub presence

## Editorial structure

The organization profile is a front door: explain the work environment, offer local and hosted routes, map the useful public repositories, and show people how to contribute or get help. Product setup detail belongs in the product repository. Research belongs in a clearly identified research section.

The profile uses Quirq's existing spectrum artwork and native GitHub text and tables. It avoids metric badges, autoplay media and third-party image services. Product names follow the current sources: **XO Space** is the environment engine and UI; **XO Swarm** is the hosted management application. The hosted application still uses the `app.xo.builders` domain.

## Reference review

Reviewed on 21 September 2026. These references inform hierarchy and usability; their prose, artwork and operating policies are not copied.

| Reference | Applied principle |
| --- | --- |
| [OpenClaw](https://github.com/openclaw/openclaw/blob/904b41e9e99f635fb8bb9920908bab9a4e5e2e5f/README.md) | Recognizable identity, direct explanation, installation and clear documentation paths. |
| [Hermes Agent](https://github.com/NousResearch/hermes-agent/blob/274bc7b8f613c299b4f59160bacf8a19010f7003/README.md) | Concrete capabilities and prominent getting-started guidance. |
| [LangChain's profile](https://github.com/langchain-ai/.github/blob/7107fd3c77cbbb20ba02653e13b2e4eb2ca3d120/profile/README.md) | Explain each repository's role and distinguish the hosted offering from open-source projects. |
| [Browser Use's profile](https://github.com/browser-use/.github/blob/521f36e3a6c21f360d606db5e8a8e0083c2b73ef/profile/README.md) | A compact invitation with contribution routes to the right repository. |
| [Supabase's community repository](https://github.com/supabase/.github/tree/5c94fa2452c1e80840835848b801c0139ad28dff) | Separate shared community guidance from product documentation. |

OpenClaw's product README is the relevant visual reference: its organization `.github` repository did not contain a profile at review time.

## Claims and destinations

- Check features against the current public release, not just a development checkout. Space was reviewed at [2a339745](https://github.com/quirq-ai/xo-space/tree/2a3397456051d96b59082dd7aa384b853ecd71b7).
- Keep execution support separate from watcher and telemetry support. Do not promise every field for every runtime.
- Describe the quirq measurement model as research. Tokens, session counts and file activity do not establish verified useful output.
- Check the hosted entry and offer before changing its call to action. Do not promise a free tier, a setup time or deployment parity without current evidence.
- `quirq_ai` contains the website and research presentation. `environment` had only a placeholder README at review time, so it is not a featured implementation destination.
- Use existing public contacts. `team@xo.builders` is the established team address; no delivery, response-time or security-service guarantee is implied by listing it.
- Add screenshots only with a source revision, capture date, privacy review and a visible statement when the data is fictional. The present header is brand artwork.

## GitHub behavior

- [Organization profiles](https://docs.github.com/en/organizations/collaborating-with-groups-in-organizations/customizing-your-organizations-profile) render `profile/README.md` from this public repository. Use absolute destinations in that file, including image sources.
- [Community defaults](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file) fill gaps. XO Space already has its own contribution guide and issue templates; these remain authoritative there.
- [Issue forms](https://docs.github.com/en/communities/using-templates-to-encourage-useful-issues-and-pull-requests/syntax-for-issue-forms) live under `.github/ISSUE_TEMPLATE/`, including in a repository named `.github`. Avoid labels or assignees that might not exist in a consuming repository.
- `SECURITY.md` does not enable [private vulnerability reporting](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/configure-vulnerability-reporting/configure-for-a-repository). The policy provides a private email route and only suggests GitHub reporting when the affected repository offers it.
- The docs repository currently has Issues and Discussions disabled. Accept documentation PRs there; route questions to the support destinations instead.
- The content workflow checks this repository only. It does not configure CI, branch protection, required reviews, repository descriptions or pinned repositories elsewhere.

## Before merging

1. Run `python scripts/validate.py` in the environment described in the root README.
2. Open every changed public destination. Check the page's purpose as well as its HTTP status; a sign-in redirect is expected for the cloud application.
3. Render the profile with GitHub-flavored Markdown and inspect light and dark themes at desktop and narrow widths. Check heading order, image loading, alternative text, table readability and horizontal overflow.
4. Check that community instructions remain usable when inherited by a different repository. Repository links should be absolute; local commands must be explicitly scoped.
5. Review the diff for unsupported claims, customer data, credentials, stale product names and new policy commitments.
6. After merging, inspect the live organization overview and issue chooser. Confirm the profile artwork resolves from `main` and the content workflow passes. Keep in mind that GitHub may cache the organization overview briefly.

## Organization settings follow-up

Repository files cannot change the organization's description or pinned projects. A suitable description is **Agent work environments, from your laptop to the cloud.** Suggested first pins are `xo-space`, `docs` and `quirq_ai`. Verify those settings separately before considering the wider organization presentation aligned; this repository makes no automatic changes to them.
