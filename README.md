# Sendery plugin

Build and migrate transactional emails with Claude Code, Cowork, or Codex. The plugin bundles Sendery's setup skill and a connection to the hosted Sendery MCP server.

- Find the SDK or framework integration that fits your application.
- Prepare templates for a new product or migrate existing transactional emails.
- Validate and preview drafts with sample data, then review them in Sendery.

A Sendery account and editing access to a project are required. Workspace limits still apply. The plugin is MIT licensed; service access is subject to your Sendery plan and terms.

## Install

### Claude Code

With the public `sendery-co/sendery-plugin` repository available:

```sh
claude plugin marketplace add sendery-co/sendery-plugin
claude plugin install sendery@sendery
```

Start a new session. Open `/mcp` to authenticate the plugin's Sendery connection if prompted, sign in, and select a project. Run `/sendery:sendery-onboarding` or ask Claude to set up Sendery.

### Claude / Cowork

Download **sendery-plugin.zip** from this repository's Releases or [Sendery's plugin download](https://sendery.co/downloads/sendery-plugin.zip). In Claude, open **Customize → Plugins** and upload the plugin ZIP. Authenticate the Sendery connection and choose a project. Use a current client with plugin support; organization settings may restrict installation.

### Codex

Add the marketplace, then install Sendery:

```sh
codex plugin marketplace add sendery-co/sendery-plugin
codex plugin add sendery@sendery
```

Alternatively, after adding the marketplace, choose **Sendery** in the desktop app's plugin browser and install it. Complete browser authorization when prompted and select a project. Start a new session to use the installed skill and tools. Requires a Codex version with plugin support.

### Local installation before public release

Unzip **sendery-marketplace.zip**, or use this repository checkout. From its parent directory:

```sh
claude plugin marketplace add ./sendery-plugin
claude plugin install sendery@sendery
```

For Codex:

```sh
codex plugin marketplace add ./sendery-plugin
codex plugin add sendery@sendery
```

Inside the Sendery application repository, use `./packages/plugin` as the marketplace path instead. These commands install the local package; they do not publish it. For a one-session Claude Code check, run `claude --plugin-dir ./plugins/sendery` from the package root.

### Other assistants

Connect a remote OAuth MCP server at **https://sendery.co/mcp**. The standalone **sendery-skill.zip** can be installed in clients supporting Agent Skills. The canonical skill is `plugins/sendery/skills/sendery-onboarding/SKILL.md`.

Use either the plugin or a manual MCP/skill installation. If you previously configured Sendery manually, remove that duplicate connection and standalone skill before using the plugin.

## Try it

> Set up Sendery for this application. Inspect the framework and existing transactional emails. Recommend the right integration, then migrate one representative email into a draft for review. Validate it and preview it using sample data. Prepare code changes without switching production delivery.

For a new app, ask for the templates your product needs. For an existing app, the skill inventories its emails, preserves variables and application logic, and migrates in small batches. It records source IDs and revisions so rerunning does not create duplicates or overwrite newer edits.

## Permissions and data

The remote connection is restricted to one project. It can read the project brand and templates, upload images, validate and save drafts, and render previews. It cannot publish, send email, modify shared branding, access billing, or read retained customer emails. Publish reviewed drafts in Sendery before switching application delivery.

No sending key belongs in the plugin. Sign-in uses OAuth with PKCE. Connections expire after 30 days and can be revoked from the project's **AI setup** page. Uninstalling the plugin does not revoke the Sendery connection; disconnect it separately when removing access.

Your assistant needs separate access to your codebase. This package does not upload a repository or install executable hooks. Selected template content, uploaded images, and preview data are sent to Sendery; tool results are visible to the connected assistant under its data policies. Use synthetic sample data and never include API keys, passwords, or real verification tokens in prompts or previews.

## Development

Python 3.10+ is needed only for packaging and tests. The installed plugin needs no Python or Node runtime.

```sh
python3 -m unittest discover -s tests
python3 tools/build.py
```

This creates reproducible plugin, marketplace, and skill ZIPs plus SHA-256 checksums in `dist/`. Only allowlisted files are included. Run `claude plugin validate ./plugins/sendery` and `claude plugin validate .` with a current Claude Code version, then test a real installation in each supported client. Source-level tests do not replace that live authentication check.

See [PUBLISHING.md](PUBLISHING.md) for repository exports, directory submissions, and release checks. Publishing a GitHub repository or release does not automatically list the plugin in either vendor's directory.

[Documentation](https://sendery.co/en/docs) · [Contact](https://sendery.co/en/contact) · [Privacy](https://sendery.co/en/privacy) · [Terms](https://sendery.co/en/terms)
