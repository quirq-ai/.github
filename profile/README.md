<p align="center">
  <a href="https://www.quirq.ai/">
    <img src="https://raw.githubusercontent.com/quirq-ai/.github/main/profile/assets/quirq-banner.png" alt="A glass ribbon refracting light into the quirq spectrum" width="100%">
  </a>
</p>

<h1 align="center">quirq</h1>

<p align="center">
  <strong>Agent work environments, from your laptop to the cloud.</strong><br>
  Give your agents a place to work. Keep projects, tools and activity in view.
</p>

<p align="center">
  <a href="https://app.xo.builders/"><strong>Open the cloud app ↗</strong></a> ·
  <a href="https://github.com/quirq-ai/xo-space#quick-start"><strong>Run Space locally</strong></a> ·
  <a href="https://docs.xo.builders/">Documentation</a> ·
  <a href="https://www.quirq.ai/">Website</a>
</p>

## A place for the work

Agent work spans repositories, runtimes and sessions. Quirq brings the environment and its project tools together, so you can:

- **Organize projects** — browse files, explore their structure and follow Git history.
- **See what's happening** — inspect project todos, recent activity and available session telemetry.
- **Connect the tools** — configure supported agents and services for the environment where you work.

## Choose your starting point

| Start here | What you get |
| --- | --- |
| **XO Space** · local<br>[Install Space →](https://github.com/quirq-ai/xo-space#quick-start) | An open-source environment engine and browser interface for your projects and agent tools. |
| **XO Swarm** · hosted<br>[Open Swarm →](https://app.xo.builders/) | A cloud application for creating, accessing and managing agent environments. |

Space provides the environment layer; Swarm provides the hosted management route. Hosted access and available applications depend on your account and environment.

Space has execution adapters for **Claude Code, Codex, OpenClaw, Hermes and Antigravity**. Session telemetry currently aggregates **Claude Code, Codex and Cursor**, with available data varying by runtime. See the [supported agents](https://github.com/quirq-ai/xo-space#supported-agents) for setup details.

### Try Space on your machine

From the directory you want to use as your workspace:

```sh
curl -fsSL https://quirq.ai/install | sh
```

Open **[localhost:5002/space/](http://localhost:5002/space/)** while the server is running. The installer requires Git and curl, sets up Python through uv, and starts Space in the foreground. Use macOS, Linux or Windows with WSL. Agent execution needs the relevant runtime and authentication.

[Installation details](https://github.com/quirq-ai/xo-space/blob/main/INSTALLATION.md) · [What leaves your machine](https://github.com/quirq-ai/xo-space#what-leaves-your-machine)

## Explore the code

| Repository | What's inside |
| --- | --- |
| [**xo-space**](https://github.com/quirq-ai/xo-space) | Environment API, agent adapters, project tools and the Space UI. |
| [**docs**](https://github.com/quirq-ai/docs) | Documentation source for Space, hosted environments and research. |
| [**quirq_ai**](https://github.com/quirq-ai/quirq_ai) | The Quirq website, research content and interactive explanations. |

[Browse all repositories →](https://github.com/orgs/quirq-ai/repositories)

## Build with us

Reproducible bug reports, documentation fixes, runtime integrations and focused improvements are welcome. Start with the repository you want to improve and follow its contribution guide.

[Contributing](https://github.com/quirq-ai/.github/blob/main/CONTRIBUTING.md) · [Space discussions](https://github.com/quirq-ai/xo-space/discussions) · [Get help](https://github.com/quirq-ai/.github/blob/main/SUPPORT.md) · [Report a security issue privately](https://github.com/quirq-ai/.github/blob/main/SECURITY.md)

## Beyond activity: useful work

Our research asks how to measure what agents deliver alongside what they consume. The **quirq** is a proposed unit of verified, human-valued work. The [whitepaper](https://www.quirq.ai/whitepaper) sets out the model, assumptions and validation questions; it is distinct from the activity and usage telemetry available in Space today.

[Read the research →](https://www.quirq.ai/research)

---

<p align="center">
  quirq · by <a href="https://xo.builders/">XO Labs</a><br>
  <a href="mailto:team@xo.builders">Contact the team</a> ·
  <a href="https://x.com/quirq_ai">Follow on X</a>
</p>
