"""Generate an n8n-themed knowledge base PDF for the AI Support Agent demo."""
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT

OUT = "n8n Knowledge Base.pdf"

styles = getSampleStyleSheet()
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=20, spaceAfter=12, textColor=HexColor("#1d4ed8"))
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=14, spaceBefore=14, spaceAfter=6, textColor=HexColor("#1e3a8a"))
h3 = ParagraphStyle("h3", parent=styles["Heading3"], fontSize=12, spaceBefore=8, spaceAfter=4, textColor=HexColor("#1e40af"))
body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10.5, leading=15, spaceAfter=6, alignment=TA_LEFT)
bullet = ParagraphStyle("bullet", parent=body, leftIndent=18, bulletIndent=6)

story = []

story.append(Paragraph("n8n — Internal Knowledge Base", h1))
story.append(Paragraph("Last updated: April 2026 &middot; For internal support use", body))
story.append(Spacer(1, 0.2 * inch))

# Section 1
story.append(Paragraph("1. What is n8n?", h2))
story.append(Paragraph(
    "n8n is a source-available workflow automation platform. It lets technical and non-technical users connect "
    "applications and APIs by composing nodes on a visual canvas. Each workflow is a directed graph of nodes that "
    "transform data step by step. n8n can run self-hosted (Docker, Kubernetes, npm) or as a managed cloud service. "
    "It supports over 400 native integrations and arbitrary HTTP calls.", body))

story.append(Paragraph("1.1 Pricing tiers", h3))
story.append(Paragraph(
    "Self-hosted n8n is free under the Sustainable Use License for internal automation. n8n Cloud has Starter, Pro, "
    "and Enterprise tiers priced by active workflow executions. Customers on the Starter plan get 2,500 executions "
    "per month; Pro gets 10,000; Enterprise is custom.", body))

# Section 2
story.append(Paragraph("2. Account &amp; access", h2))

story.append(Paragraph("2.1 Resetting your password", h3))
story.append(Paragraph(
    "If you forgot your n8n password, go to the login page and click \"Forgot password?\". Enter your email and we "
    "will send a reset link valid for 60 minutes. The reset email comes from no-reply@n8n.io. If you do not receive "
    "it within 5 minutes, check your spam folder. If still missing, contact support and we can issue a manual reset.", body))

story.append(Paragraph("2.2 Two-factor authentication (2FA)", h3))
story.append(Paragraph(
    "Enable 2FA from Settings &gt; Personal &gt; Two-factor authentication. We support TOTP apps (Authy, Google "
    "Authenticator, 1Password). Backup codes are shown once at setup &mdash; save them. Lost both your phone and "
    "backup codes? Support can disable 2FA after identity verification, which takes 24&ndash;48 hours.", body))

story.append(Paragraph("2.3 SSO and SAML", h3))
story.append(Paragraph(
    "SAML SSO is available on Enterprise plans only. Configure it under Settings &gt; SSO. Supported providers "
    "include Okta, Azure AD, Google Workspace, and OneLogin. SCIM provisioning is in beta and available on request.", body))

# Section 3
story.append(Paragraph("3. Workflows", h2))

story.append(Paragraph("3.1 Creating a workflow", h3))
story.append(Paragraph(
    "Click \"+ New Workflow\" in the left sidebar. Add a trigger node (Webhook, Cron, App-specific Trigger), then "
    "chain processing and output nodes. Save with Ctrl+S. A workflow runs only when both Active is toggled on and "
    "its trigger fires.", body))

story.append(Paragraph("3.2 Sharing workflows", h3))
story.append(Paragraph(
    "On Pro and Enterprise plans, workflows can be shared with specific users or projects. Click the share icon at "
    "the top of the canvas. Sharing requires the recipient to have a seat in the same instance. Cross-instance "
    "sharing is not supported &mdash; export to JSON and import on the other side.", body))

story.append(Paragraph("3.3 Activating a workflow", h3))
story.append(Paragraph(
    "Toggle the Active switch in the top-right of the editor. Once active, the trigger starts listening or polling. "
    "Schedule and Cron triggers fire only when active. A common pitfall: editing an active workflow does not "
    "auto-republish in older versions &mdash; click Save explicitly.", body))

# Section 4
story.append(Paragraph("4. Credentials", h2))
story.append(Paragraph(
    "Credentials are stored encrypted at rest using the encryption key set in your environment. Each credential is "
    "scoped to its owner by default; share via Settings &gt; Credentials. We never log credential values, and they "
    "are redacted in execution logs.", body))

story.append(Paragraph("4.1 Rotating a credential", h3))
story.append(Paragraph(
    "Open Credentials &gt; the credential &gt; Edit &gt; paste the new token. All workflows using that credential "
    "pick up the new value on next execution. There is no downtime. If the old token leaked, rotate it at the "
    "provider first, then update n8n.", body))

story.append(Paragraph("4.2 OAuth re-authorization", h3))
story.append(Paragraph(
    "OAuth credentials (Google, Slack, Microsoft) expire when the upstream token revokes or when you change scopes. "
    "Open the credential and click Reconnect. If the connect button is greyed out, your instance OAuth callback URL "
    "may have changed &mdash; verify N8N_HOST and WEBHOOK_URL.", body))

# Section 5
story.append(Paragraph("5. Self-hosting", h2))

story.append(Paragraph("5.1 Recommended deployment", h3))
story.append(Paragraph(
    "We recommend Docker on a Linux VPS with at least 2 vCPU, 4 GB RAM, and 20 GB disk for production. Front it "
    "with nginx or Caddy for HTTPS. Use Postgres (not SQLite) once you exceed ~50 active workflows. Set "
    "N8N_ENCRYPTION_KEY to a stable value &mdash; if it changes, all credentials become unreadable.", body))

story.append(Paragraph("5.2 Backups", h3))
story.append(Paragraph(
    "Back up the Postgres database (or the SQLite file at /home/node/.n8n/database.sqlite) and the "
    "/home/node/.n8n directory. Store the encryption key separately. To restore: install n8n, place the key in env, "
    "restore the DB, restart.", body))

story.append(Paragraph("5.3 Upgrading", h3))
story.append(Paragraph(
    "Pull the latest Docker image and restart the container. Migrations run automatically. Major version upgrades "
    "are documented in the changelog at docs.n8n.io. Always back up before upgrading. If a workflow stops working "
    "after upgrade, check the node version &mdash; n8n keeps old versions available, switch back manually.", body))

# Section 6
story.append(Paragraph("6. Billing", h2))

story.append(Paragraph("6.1 Execution counting", h3))
story.append(Paragraph(
    "An execution is one full workflow run, regardless of how many nodes it contains. Failed executions still count. "
    "Manual test executions on Cloud do count against quota. Sub-workflow runs count as one extra execution per "
    "invocation.", body))

story.append(Paragraph("6.2 Updating payment method", h3))
story.append(Paragraph(
    "Go to Settings &gt; Billing &gt; Payment methods. Add the new card, set as default, then remove the old one. "
    "Invoices are emailed monthly to the billing email on file.", body))

story.append(Paragraph("6.3 Refunds", h3))
story.append(Paragraph(
    "Pro-rated refunds are available within 14 days of the most recent invoice. Submit a refund request via support "
    "with the invoice number. Approved refunds appear in 5&ndash;10 business days.", body))

# Section 7
story.append(Paragraph("7. Common errors", h2))

story.append(Paragraph("7.1 \"Webhook node not registered\"", h3))
story.append(Paragraph(
    "This happens when a webhook workflow is not active. Activate the workflow and the URL becomes live. The "
    "production URL is different from the test URL &mdash; the test URL is only valid while the canvas is open and "
    "Listen for Test Event is clicked.", body))

story.append(Paragraph("7.2 \"Could not get parameter dependencies\"", h3))
story.append(Paragraph(
    "Usually means a credential is missing or expired. Open the failing node, rebind the credential. If still "
    "failing, the upstream API may have rate-limited &mdash; check the response body in the execution log.", body))

story.append(Paragraph("7.3 Workflow stuck in \"Running\"", h3))
story.append(Paragraph(
    "Likely a long HTTP request or an infinite loop. Check execution logs for the last node. If it is hung on an "
    "external API call, increase the timeout under node Settings &gt; Options &gt; Timeout. To force-stop, restart "
    "the n8n process &mdash; in Docker that is &lt;code&gt;docker compose restart n8n&lt;/code&gt;.", body))

# Section 8
story.append(Paragraph("8. Contacting support", h2))
story.append(Paragraph(
    "Email support@n8n.io for non-urgent issues; expect a response within 1 business day on Starter, 4 hours on "
    "Pro, and 1 hour on Enterprise (during business hours). For urgent production outages on Enterprise, use the "
    "on-call phone line printed in your contract. Self-hosted users can also ask in the community forum at "
    "community.n8n.io &mdash; many staff members are active there.", body))

doc = SimpleDocTemplate(OUT, pagesize=LETTER, leftMargin=0.8*inch, rightMargin=0.8*inch, topMargin=0.8*inch, bottomMargin=0.8*inch)
doc.build(story)
print(f"Wrote {OUT}")
