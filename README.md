# Build transactional emails with Sendery and AI

Create or migrate transactional emails with your AI assistant. Preview them in Sendery and give your team templates they can edit without changing application code.

- Turn existing emails into editable templates.
- Adjust copy, design, and translations with your assistant.
- Connect your app with the Sendery SDK or framework integration that fits it.
- Connect app events and prepare trigger flows with their email templates.

## Get started

Create a Sendery project and open your app’s repository in your coding assistant. You’ll need permission to edit the project’s templates.

### Claude Code

Run this in your terminal:

```sh
claude mcp add --transport http sendery https://sendery.co/mcp
```

In Claude Code, run `/mcp`, sign in to Sendery, and select your project.

Add the Sendery skill from your repository root:

```sh
mkdir -p .claude/skills/sendery-onboarding
curl -fsSL 'https://sendery.co/developer-tools/sendery-onboarding/SKILL.md' -o .claude/skills/sendery-onboarding/SKILL.md
```

[Claude Code guide](https://sendery.co/en/docs/claude-code)

### OpenAI Codex

Run these commands in your terminal, then sign in to Sendery in the browser and select your project:

```sh
codex mcp add sendery --url https://sendery.co/mcp
codex mcp login sendery
```

Add the Sendery skill from your repository root:

```sh
mkdir -p .agents/skills/sendery-onboarding
curl -fsSL 'https://sendery.co/developer-tools/sendery-onboarding/SKILL.md' -o .agents/skills/sendery-onboarding/SKILL.md
```

[Codex guide](https://sendery.co/en/docs/codex)

### Other assistants

Add `https://sendery.co/mcp` as a remote MCP server using OAuth browser sign-in. Sign in and select your Sendery project, then add the [Sendery skill](https://sendery.co/developer-tools/sendery-onboarding/SKILL.md) to your client or share its contents with your assistant.

[Other MCP clients guide](https://sendery.co/en/docs/mcp-clients)

## Tell your assistant what to build

Name the emails you want to create or migrate, and include any branding or languages you want to keep. Start with this prompt:

> Set up Sendery for this application. Inspect the framework and existing transactional emails, then recommend the simplest compatible integration. For a new app, prepare the templates we need. For an existing app, follow my requested migration scope; if I have not chosen emails, summarize them and ask which to migrate. You may suggest starting with one for review. Validate and preview the drafts with sample data. Replace the old sending paths for migrated emails without adding on/off flags or fallback senders. Guide me through adding the sending API key to my local environment and deployment secrets without sharing it in chat or committing it. Explain your changes, tests, draft links, and any remaining setup or publishing steps.

You can start with one email or migrate them all. See [Migrate transactional emails to Sendery with AI](https://sendery.co/en/docs/ai-migration) for a walkthrough.

## Connect app events

Open **Triggers → App connection → Set up with MCP** in Sendery. Connect your assistant to the project, then use the event setup prompt to inspect your app and choose which events to connect.

The assistant can register app events, validate sample payloads, and prepare trigger flows with their email drafts, timing, and conditions. It returns editor links for review and publication in Sendery. Configure the project API key in your app’s server environment and test the connection in Sandbox. Existing assistant connections need to reconnect to approve app event and trigger draft access.

## Preview, publish, and send

Your assistant prepares editable drafts with sample data. Open **AI Setup** in your Sendery project to review them, or ask for changes to the copy and design.

Publish the templates when you’re ready. Create a [project API key](https://sendery.co/en/docs/authentication), add it to your app’s environment settings, and follow [Send your first email](https://sendery.co/en/docs/quickstart) to test the integration.

Your team can then update the templates in Sendery without editing application code.

## Your control

The Sendery connection can edit email and trigger drafts, generate email previews, register app event definitions, and validate sample events. It cannot publish templates or triggers, send emails, or access billing or saved email content. Disconnect it from **AI Setup → Connected assistants** at any time.

[Documentation](https://sendery.co/en/docs) · [Support](https://sendery.co/en/contact) · [Privacy](https://sendery.co/en/privacy) · [Terms](https://sendery.co/en/terms)

[MIT license](LICENSE).
