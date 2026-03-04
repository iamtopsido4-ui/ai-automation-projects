AI Automation Portfolio
A collection of production-ready n8n workflows built for real business use cases. Each workflow is plug-and-play and uses Claude (Anthropic) AI for intelligent automation.

Workflows
✅ Workflow 1 — AI Email Responder
File: workflow-1-ai-email-responder.json
Automatically drafts AI-generated replies to incoming emails and saves them as Gmail drafts for review before sending.
Tools used: Gmail · Anthropic Claude
Flow:
Gmail Trigger → Claude AI → Gmail Create Draft
Business value: Saves hours of email handling time. Ideal for customer support, sales, and operations teams.

✅ Workflow 2 — Google Sheets Lead Enricher
File: workflow-2-lead-enricher.json
Watches a Google Sheet for new leads. When a new row is added with a name and company, Claude AI automatically generates a company summary and personalized sales pitch, then writes the results back to the sheet.
Tools used: Google Sheets · Anthropic Claude
Flow:
Google Sheets Trigger → Claude AI → Code (Parse JSON) → Google Sheets Update Row
Business value: Eliminates manual lead research. Sales teams get instant, personalized pitch suggestions for every new lead.


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
