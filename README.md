# MindForge - Multi Agent Research System

Impact: Automates an iterative research workflow to produce evidence-backed, polished reports faster.

A Streamlit-based multi-agent research system that searches the web, scrapes the most relevant source, drafts a report, and then critiques it for quality.

## What it does

- Search agent finds recent, reliable sources for a topic.
- Reader agent scrapes the most relevant result for deeper content.
- Writer chain turns the gathered research into a structured report.
- Critic chain reviews the report and returns feedback.
- Revision chain applies critic feedback to produce the final improved report.
- Uses a multi-agent feedback loop (writer → critic → revision) to iteratively improve report quality.

## Project files

- `app.py` - Streamlit UI
- `pipeline.py` - CLI pipeline runner
- `agents.py` - LLM setup, agents, writer, and critic chains
- `tools.py` - Search and scraping tools
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

## Requirements

- Python 3.10 or newer
- A virtual environment is recommended
- API keys for the external services you want to use

## Environment variables

Create a `.env` file with the keys below:

```env
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

The app uses Gemini and Groq model fallbacks, so having both `GOOGLE_API_KEY` and `GROQ_API_KEY` available is recommended.

## Setup

1. Create and activate a virtual environment.

	 - Windows (PowerShell):

		 ```powershell
		 python -m venv .venv
		 .\.venv\Scripts\Activate.ps1
		 ```

	 - macOS / Linux (bash):

		 ```bash
		 python3 -m venv .venv
		 source .venv/bin/activate
		 ```
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Add your API keys to `.env`.

## Run the app

### Streamlit UI

```bash
streamlit run app.py
```

### Command-line pipeline

```bash
python pipeline.py
```

## Notes

- The search tool uses Tavily for web search.
- The reader tool scrapes the selected URL using multiple extraction strategies.
- The pipeline prints each stage to the console so you can follow the workflow.

