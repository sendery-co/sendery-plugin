# Publishing Sendery

## Package layout

Both platform manifests live in `plugins/sendery`. They share one `.mcp.json`, skill, and assets. `.agents/plugins/marketplace.json` is the Codex catalog; `.claude-plugin/marketplace.json` is the Claude catalog. Relative paths are rooted at this repository, so it can be exported independently of the application.

## Prepare a release in the application repository

1. Update the version in both plugin manifests and `CHANGELOG.md` together. Never reuse a published version.
2. Run:

   ```sh
   python3 -m unittest discover -s packages/plugin/tests
   python3 packages/plugin/tools/build.py
   python3 packages/plugin/tools/build.py --output public/downloads
   python3 packages/plugin/tools/build.py --output public/downloads --check
   python3 -m unittest discover -s packages/tools
   ```

3. Review and commit the package, tests, updated public ZIPs, and integration changes. The website serves these committed archives without needing Python in production.
4. Create the empty public GitHub repository **sendery-co/sendery-plugin**. Inspect the subtree export, then push only that subtree:

   ```sh
   python3 packages/tools/export.py plugin
   python3 packages/tools/export.py plugin --push
   ```

   The export tool rejects uncommitted package files and never pushes the application's branch. Do not publish the private application repository. To incorporate public contributions first:

   ```sh
   git subtree pull --prefix=packages/plugin git@github.com:sendery-co/sendery-plugin.git main
   ```

5. Wait for the standalone repository's checks. Test real installations in Claude and Codex against the deployed MCP server.
6. Create a GitHub Release on that repository's main branch using the matching `vX.Y.Z` tag. The release workflow builds and attaches three ZIPs and `SHA256SUMS`. It does not submit to vendor directories. No npm/PyPI/Composer publication is needed.

## Live prerequisites

- Deploy the MCP and OAuth routes, migrations, and stable Passport signing keys. Configure the correct HTTPS application URL.
- Check `https://sendery.co/.well-known/oauth-authorization-server` and `https://sendery.co/.well-known/oauth-protected-resource/mcp`.
- Complete browser consent, select a project, and exercise draft creation, preview, and disconnect in both clients. Verify that real callback origins match the explicit redirect allowlist; never use a wildcard to pass review.
- Test refresh and reconnection after expiry. Remove any manually installed duplicate Sendery server/skill when testing the plugin.
- Use a dedicated reviewer account and project containing synthetic examples. Never publish reviewer credentials in the repository or ZIPs. Supply them privately through the submission portals.
- Ensure public privacy, terms, support, and publisher details are accurate. Replace any unresolved legal operator placeholders before public directory submission. Confirm account/provider availability before selecting supported countries.

## Listing copy

**Name:** Sendery

**Short description:** Build and migrate transactional email templates.

**Description:** Connect your project to build email templates and integrate Sendery with your application. Find a compatible SDK, migrate existing transactional emails, and validate drafts with sample previews. Review and publish templates in the Sendery editor.

**Website:** https://sendery.co

**Documentation:** https://sendery.co/en/docs

**Support:** https://sendery.co/en/contact

**Privacy:** https://sendery.co/en/privacy

**Terms:** https://sendery.co/en/terms

**MCP endpoint:** https://sendery.co/mcp

**Authentication:** OAuth authorization code with PKCE S256; scope `mcp:use`; project selected at browser consent.

**Logo:** `plugins/sendery/assets/logo.png`

**Prompts:** See `interface.defaultPrompt` in the Codex manifest.

## Directory submissions

### Claude

Use the [Claude directory submission portal](https://claude.com/blog/build-plugins-for-claude). Submit a plugin bundle using the public GitHub repository and point reviewers to `plugins/sendery`. The bundle combines the remote MCP server and the migration skill. If the portal requires a plugin-root archive, use `sendery-plugin.zip`. Review approval and your subsequent publication are separate steps.

### OpenAI

Follow [plugin submission](https://developers.openai.com/plugins/deploy/submission). Submit **With MCP**, with the universal production URL and the skill bundle. Prepare a verified publisher identity, domain verification, public policy links, and private demo credentials. Use the available package/upload format requested by the portal; `sendery-plugin.zip` includes the Codex manifest and `sendery-skill.zip` contains the standalone skill.

The server's save-draft tool is a write operation that can replace an existing draft; its destructive annotation reflects that. Image uploads are writes. Read/validate/preview tools are read-only. Do not describe this integration as capable of live sending, publishing, billing access, or retrieving stored recipient emails.

After approval, publish from the portal to make the listing available. A local marketplace or GitHub Release alone does not create a public directory listing.

## Reviewer test cases

Run these with a synthetic project and repository. Record client versions and actual outcomes before submission; the table specifies expected outcomes, not completed manual tests.

| Case | Prompt/action | Expected result |
| --- | --- | --- |
| New application | “Inspect this Laravel app and prepare a welcome email in Sendery.” | Compatible integration recommended; valid unpublished draft and editor link; no production sending change. |
| Existing application | “Inventory these transactional emails and migrate the order confirmation first.” | Variables and logic preserved; unsupported features flagged; one draft saved. |
| Preview | “Preview the welcome email for Mika using an example.com action URL.” | Subject, HTML, and text use synthetic data; no email sent. |
| Resume | Repeat the identical migration using its original source ID. | Same template and revision returned; no duplicate. |
| Image | Upload an authorized small PNG and use it in a draft. | Project image created and referenced; preview shows it. |
| Cross-project access | Request a template ID owned by another project. | Access denied/not found; no other project's data returned. |
| Conflicting edit | Edit a draft in Sendery, then retry an older import without the new revision. | Conflict returned; human edits preserved. |
| Forbidden actions | “Publish this now and send it to a real customer.” | No publishing or sending tool available; assistant directs user to review in Sendery. |
| Disconnect | Disconnect in AI setup, then retry an authenticated tool call. | Old connection cannot access the project; requires new consent. |

For codebase migration, also compare a representative original and imported preview visually on desktop and mobile. Repository access is provided by the user's assistant, not by the Sendery connection.
