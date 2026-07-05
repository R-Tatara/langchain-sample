<!-- Badges -->
[![MIT](https://custom-icon-badges.herokuapp.com/badge/license-MIT-8BB80A.svg?logo=law&logoColor=white)]()
[![Python](https://custom-icon-badges.herokuapp.com/badge/Python-3572A5.svg?logo=Python&logoColor=white)]()

# langchain-sample

A LangChain sample project exploring LLM agent patterns with Google Gemini. It demonstrates plain invoke/streaming calls, structured output parsing, and a read-only SQL agent backed by a local SQLite database.

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- A Google Gemini API key

## Installation

```bash
git clone https://github.com/R-Tatara/langchain-sample.git
cd langchain-sample
uv sync
```

## Configuration

Set your Gemini API key as an environment variable:

```bash
export GOOGLE_API_KEY="your-api-key"
```

## Database Setup

The SQL agent queries a local SQLite database (`sample.db`). Create it before running the agent:

```bash
uv run python init_db.py
```

## Usage

```bash
uv run python main.py
```

## LISENCE

MIT
