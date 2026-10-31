# Autonomous Multi-Agent Research System

A Streamlit research assistant that coordinates search, page reading, report writing, and critic review through a multi-step agent pipeline.

## Workflow

1. Search agent gathers recent information about a user-supplied topic.
2. Reader agent selects a relevant result and extracts deeper content.
3. Writer chain drafts a report from the gathered material.
4. Critic chain reviews the generated report and returns feedback.

The Streamlit interface presents the report, critic feedback, search results, and scraped content in separate tabs.

## Run locally

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Environment

Configure the API credentials required by the agent/provider implementations in your local environment or hosting dashboard. Common configuration includes:

- `OPENAI_API_KEY`
- `TAVILY_API_KEY` (if the search implementation uses Tavily)

Never commit real API keys. Use a local `.env` file only if the project loads it, and keep it out of version control.

## Deploy on Render

The repository includes a `render.yaml` blueprint for a Python Streamlit web service. Add the required secrets in the Render dashboard before using the app.

## Notes

- Search and scraped-page content depend on external providers and network availability.
- Review generated reports and source material before relying on them.
- Add tests for agent outputs, provider failures, and malformed search results before production use.
