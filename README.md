AI Automation Portfolio
A collection of production-ready n8n workflows built for real business use cases. Each workflow is plug-and-play and uses Claude (Anthropic) AI for intelligent automation.

Workflows
Workflow 1 — AI Email Responder
File: workflow-1-ai-email-responder.json
Automatically drafts AI-generated replies to incoming emails and saves them as Gmail drafts for review before sending.
Tools used: Gmail · Anthropic Claude
Flow:
Gmail Trigger → Claude AI → Gmail Create Draft
Business value: Saves hours of email handling time. Ideal for customer support, sales, and operations teams.

Workflow 2 — Google Sheets Lead Enricher
File: workflow-2-lead-enricher.json
Watches a Google Sheet for new leads. When a new row is added with a name and company, Claude AI automatically generates a company summary and personalized sales pitch, then writes the results back to the sheet.
Tools used: Google Sheets · Anthropic Claude
Flow:
Google Sheets Trigger → Claude AI → Code (Parse JSON) → Google Sheets Update Row
Business value: Eliminates manual lead research. Sales teams get instant, personalized pitch suggestions for every new lead.

Workflow 3 — Customer Support Ticket Classifier
File: workflow-4-support-ticket-classifier.json
Receives customer support submissions via webhook, uses Claude to classify urgency and category, routes each ticket to the correct Google Sheet tab via a Switch node, and sends an automatic reply email to the customer.
Tools used: Webhook · Anthropic Claude · Switch Node · Google Sheets · Gmail
Flow:
Webhook → Claude AI → Code (Parse JSON) → Switch
                                            ├── Urgent  → Sheets: Urgent tab  ──┐
                                            ├── Billing → Sheets: Billing tab ──┤→ Gmail
                                            └── General → Sheets: General tab ──┘
Business value: Eliminates manual ticket sorting. Support teams instantly see prioritized, categorized tickets with customers getting immediate auto-replies.

Workflow 4 — Daily AI Business Briefing
File: Workflow-5-daily-standup.json`

Every morning at 8am, pulls active tasks from Google Sheets, generates an intelligent daily standup report with priorities, risks, and a motivational message, then sends it via Gmail and logs it to Google Docs.

Tools used:  Schedule Trigger · Google Sheets · Anthropic Claude · Gmail · Google Docs

Flow:
Schedule Trigger → Google Sheets → Code (Format Tasks) → Claude AI → Code (Parse JSON) → Gmail → Google Docs

Business value: Teams start every day with a smart, auto-generated briefing. No more manual standup prep or missed priorities.




How to Use

Clone or download this repo
Open your n8n instance
Click Import → select the workflow JSON file
Add your credentials (Anthropic API key, Gmail, Google Sheets)
Activate the workflow


Setup Requirements

n8n (self-hosted or cloud)
Anthropic API key — get one here
Google account with Gmail and Google Sheets access


About
Built as part of a structured AI automation learning path focused on real-world business workflows.
