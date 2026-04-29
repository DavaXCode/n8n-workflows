# n8n Workflows That Actually Ship

Real automation, not demos. Each workflow here runs in production — scoring leads, booking calls, answering Slack questions from a vector DB. Drop the JSON into any n8n instance and it works.

---

## What's inside

### [AI Inbox](./AI%20Inbox/) — *the thing that would have replied to your email*
Gmail trigger → LLM classifies intent → meeting requests get a calendar-aware draft offering 3 free slots in your timezone, leads get logged to a Sheet plus a polite acknowledgement draft, spam gets labeled and skipped. **Drafts only — a human reviews before sending.** Idempotent via Gmail labels, no second state store.
**Stack:** Gmail Trigger · Groq (Llama 3.3 70B) · Google Calendar · Google Sheets · Slack *(optional)*

### [Lead Funnel](./Lead%20Funnel/) — *live on my portfolio*
A contact form → AI scoring → tiered email → Slack alert → Cal.com booking → cron reminders pipeline. Three coordinated flows, one Google Sheet acting as the CRM.
**Stack:** Webhook · Groq (Llama 3.3 70B) · Gmail · Slack · Google Sheets · Cal.com · cron

### [RAG](./Rag/) — *Slack-queryable knowledge base*
Drop in a PDF, ask a question in Slack, get an answer cited from your own docs. Embeddings via Jina, vectors in pgvector, generation by Groq, deferred-response pattern so Slack's 3-second budget is never blown.
**Stack:** Webhook · Jina embeddings (1024-dim) · PostgreSQL + pgvector · Groq · Slack slash commands

### [AI Support Agent](./AI%20Support%20Agent/) — *Telegram bot with tools, not just prompts*
Inbound Telegram message → n8n AI Agent (Groq Llama 3.3 70B) with three first-class tools: `search_knowledge_base` (calls the RAG workflow over HTTP), `Create Support Ticket` (Notion), `Escalate To Human` (Slack). Postgres-backed conversation memory keyed by `chat.id`. Composes the existing RAG as a tool — the agent decides when to retrieve, when to open a ticket, when to page a human.
**Stack:** Telegram Bot API · n8n AI Agent · Groq (Llama 3.3 70B) · PostgreSQL chat memory · Notion · Slack · Jina + pgvector (via RAG)

### [Slack → Telegram Bridge](./Slack%20Telegram%20Bridge/) — *closes the escalation loop*
The other half of the AI Support Agent. When a human replies in a Slack thread under an escalation post, this workflow extracts the original Telegram chat ID from the parent message and forwards the reply back to the user — turning one-way escalations into real two-way conversations. Stateless: the chat ID is stamped into the escalation post itself, no DB lookup needed.
**Stack:** Slack Events · `conversations.history` · Telegram Bot API

### [Trading Bot](./Trading%20Bot/) — *operational scaffolding around a redacted strategy*
Cron scanner + 15-min watch loop + Telegram-driven `/analyze`, `/portfolio`, `/history` bot + session-end auto-close on Bybit. The strategy itself is stubbed out — what's exposed is the production plumbing: Notion as trade journal, Postgres paper-trade shadow, daily-loss + open-position guards, force-close at session end.
**Stack:** Cron · Bybit V5 (HMAC-signed) · Notion · PostgreSQL · Telegram bot

---

## Try one in 60 seconds

```bash
# 1. n8n → Workflows → Import from File → pick the .json
# 2. Bind your credentials on the red-flagged nodes
# 3. Activate → hit the webhook
curl -X POST https://<your-n8n>/webhook/lead-funnel -d '{...}'
```

Each folder has a `README.md` with the exact payloads, schema, and credential list.

---

## Repo layout

```
n8n/
├── AI Inbox/
│   ├── AI Inbox — Triage & Draft.json
│   └── README.md
├── Lead Funnel/
│   ├── Lead Funnel — B2B Portfolio.json
│   └── README.md
├── Rag/
│   ├── RAG — Ingestion.json
│   ├── RAG — Slack Channel Ingestion.json
│   ├── RAG — Query.json
│   ├── RAG — Query (HTTP).json
│   └── README.md
├── AI Support Agent/
│   ├── AI Support Agent — Telegram.json
│   ├── n8n Knowledge Base.pdf
│   └── README.md
├── Slack Telegram Bridge/
│   ├── Slack — Telegram Bridge.json
│   └── README.md
├── Trading Bot/
│   ├── BTMS — Scan & Watch.json
│   ├── BTMS — Unified Bot.json
│   └── README.md
└── README.md
```

---

## Sanitized for sharing

Tokens, Sheet IDs, and instance-specific values are replaced with `YOUR_*` placeholders or `$env.*` references. Nothing here will leak into your n8n if you forget to swap a value — it just won't run.

One footgun worth calling out: the Lead Funnel uses a raw HTTP node for one Slack call that reads `$env.SLACK_BOT_TOKEN`. Set it on your host, or swap that node for a native Slack node bound to your credential.

---

## Why these are worth reading

- **Label-as-state idempotency** — AI Inbox uses Gmail's own `ai-triaged` label as the dedup marker; no Redis, no Sheet, no separate processed-message table
- **Drafts, not auto-send** — AI Inbox classifies and writes the reply but always leaves it in Drafts; a wrong auto-reply is more expensive than a wrong draft
- **Calendar slots computed locally, not asked of the LLM** — Free/Busy + Luxon decides which slots are real; the LLM only writes the prose around them
- **Idempotent crons** — the reminder loop uses a `Reminded` flag in Sheets as the dedup key, no extra state store
- **AI parsing that doesn't blow up** — structured-output schema *plus* a default fallback if the model returns garbage
- **Slack-friendly RAG** — ack within 3 s, generate async, post via `response_url` so slash commands feel instant
- **RAG composed as an agent tool** — AI Support Agent calls a synchronous HTTP variant of RAG (`/webhook/rag-query` returning `{answer, sources}`) so the LLM can decide *when* to retrieve, instead of forcing every message through the vector store
- **`$fromAI` for tool arguments** — Notion ticket fields (summary, priority, details) and the Slack escalation text are filled by the LLM at tool-call time, not hardcoded; the agent owns the phrasing and severity
- **Per-user conversation memory** — Postgres chat memory keyed by Telegram `chat.id` keeps each user's context isolated without bespoke session plumbing
- **Three pipelines / one workflow** in Lead Funnel — kept together because they share credentials and a Sheet; splitting would multiply config without separating concerns
- **Defensive escaping on raw SQL** — single quotes are pre-escaped before interpolation; production-grade rewrite would move to parameterized queries

---

## Stack

| Layer | Tool |
| --- | --- |
| Orchestration | n8n (self-hosted, Docker on Linux VPS, nginx) |
| LLM | Groq — Llama 3.3 70B |
| Embeddings | Jina AI — `jina-embeddings-v3` @ 1024-dim |
| Vector DB | PostgreSQL 16 + `pgvector` (HNSW index) |
| Channels | Gmail · Google Calendar · Slack · Google Sheets · Cal.com · generic webhooks |

---

## Contact

**Andrei Mar Dava** — AI Automation & Full-Stack Engineer
[Portfolio](https://andrei.figliounicotech.online) · [LinkedIn](https://www.linkedin.com/in/andrei-mar-dava-55a64a339) · davaxdev@gmail.com
