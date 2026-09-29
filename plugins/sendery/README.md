# Sendery plugin

Connect your AI assistant to a Sendery project to build email templates, migrate existing transactional emails, and preview drafts.

## Install

In Claude or Cowork, open **Customize → Plugins** and upload the plugin ZIP. In Claude Code or Codex, use the marketplace instructions in the [repository README](https://github.com/sendery-co/sendery-plugin#install). Requires a client version that supports plugins and remote HTTP MCP with OAuth.

Sign in to Sendery when prompted and choose one project. If Claude Code shows the server as disconnected, open `/mcp` and authenticate the plugin's Sendery connection. No sending API key is needed.

Try: **“Set up Sendery for this application. Inspect the framework and existing emails, then prepare one template for review.”** In Claude Code, the skill is `/sendery:sendery-onboarding`.

## Access

The plugin can read project branding and templates, upload images, save drafts, and preview with sample data. It cannot publish, send email, change shared branding, or read billing or retained customer emails. Review and publish drafts in Sendery.

Your coding assistant needs access to the code you want it to migrate. Connecting Sendery does not grant repository access. Use synthetic preview data. Template content and previews returned by Sendery are visible to your assistant under its own data policies.

Disconnect in the project's **AI setup** page. Connections expire after 30 days. Uninstalling the plugin is separate from revoking its Sendery connection. If you previously connected Sendery manually, remove that duplicate MCP connection and standalone skill before using the plugin.

[Documentation](https://sendery.co/en/docs) · [Support](https://sendery.co/en/contact) · [Privacy](https://sendery.co/en/privacy) · [Terms](https://sendery.co/en/terms)

Plugin files are MIT licensed; Sendery service access is subject to its terms and your workspace plan.
