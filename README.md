# MindForge - Multi Agent Research System

A Streamlit-based multi-agent research system that searches the web, scrapes the most relevant source, drafts a report, critiques it for quality, and refines it based on feedback.

## What it does

- Search agent finds recent, reliable sources for a topic.
- Reader agent scrapes the most relevant result for deeper content.
- Writer chain turns the gathered research into a structured report.
- Critic chain reviews the report and returns feedback.
- Revision chain applies critic feedback to produce the final improved report.
- Uses a multi-agent feedback loop (writer → critic → revision) to iteratively improve report quality.

## Project files

- `app.py` - Streamlit UI with live pipeline visualization
- `pipeline.py` - CLI pipeline runner for batch processing
- `agents.py` - LLM setup (Gemini with Groq fallbacks), search agent, writer/critic/revision chains
- `tools.py` - Web search (Tavily) and content scraping utilities
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules
- `LICENSE` - Project license

## Requirements

- Python 3.11 or newer
- A virtual environment is recommended
- API keys for Gemini, Groq, and Tavily (see Environment variables below)

## Environment variables

Create a `.env` file with the keys below:

```env
TAVILY_API_KEY=your_tavily_api_key
GOOGLE_API_KEY=your_google_api_key
GROQ_API_KEY=your_groq_api_key
```

The app uses **Google Gemini as the primary model** with Groq fallbacks (Llama 3.3, DeepSeek-R1, and Llama 3.1). Having all three API keys available ensures seamless fallback execution if one service is unavailable.

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

- **Web Search:** Uses Tavily API for reliable, up-to-date search results.
- **Content Extraction:** The scraper employs multiple strategies (BeautifulSoup, Readability, Trafilatura) to extract clean, readable content from web pages.
- **Multi-Agent Workflow:** Features a feedback loop where the Critic evaluates the Writer's draft, and the Revision agent applies the feedback to produce a polished final report.
- **Model Fallbacks:** If the primary Gemini model is unavailable, the system automatically falls back to Groq models with progressive downgrades based on availability.
- **Console & Web UI:** Pipeline execution prints detailed stages to console (CLI) and displays real-time progress in the Streamlit web interface (UI).