# 📝 AI Content Crew

A multi-agent AI system that researches, writes, and edits blog articles on any topic — built with [CrewAI](https://www.crewai.com/), Groq-hosted open-source LLMs, and live web search.

**🔗 Live app:** _[https://ai-content-crew-xwjamzcdazi6nxc9ncn3ed.streamlit.app/]_

---

## How it works

Three AI agents collaborate in sequence, each with its own role, goal, and personality:

1. **Content Planner** 🔍 — researches the topic using real-time web search (via Serper), identifies the target audience, and builds a structured content outline with SEO keywords and sources.
2. **Content Writer** ✍️ — takes the Planner's outline and drafts a full, engaging blog post.
3. **Editor** ✅ — proofreads the draft for grammar, tone, and journalistic balance, and produces the final publish-ready article.

Each agent's output automatically becomes context for the next, so the final article reflects genuine research rather than the LLM's memorized training data.

## Features

- 🌐 **Live web search grounding** — the Planner pulls current information from Google search results rather than relying on the LLM's (potentially outdated) training data.
- 🎯 **Per-role temperature tuning** — the Planner and Editor stay factual and precise (low temperature), while the Writer gets more creative freedom (higher temperature).
- 📄 **Downloadable output** — generated articles can be saved directly as Markdown.
- ⚡ **Fast inference** — powered by Groq's LPU inference for the `llama-3.3-70b-versatile` model.

## Tech stack

| Layer | Tool |
|---|---|
| Multi-agent orchestration | [CrewAI](https://www.crewai.com/) |
| LLM inference | [Groq](https://groq.com/) (Llama 3.3 70B) |
| Provider routing | [LiteLLM](https://www.litellm.ai/) |
| Web search | [Serper](https://serper.dev/) |
| Frontend / deployment | [Streamlit](https://streamlit.io/) + Streamlit Community Cloud |

## Running locally

```bash
git clone https://github.com/YOUR_USERNAME/ai-content-crew.git
cd ai-content-crew
pip install -r requirements.txt
streamlit run app.py
```

You'll need free API keys from [Groq](https://console.groq.com/keys) and [Serper](https://serper.dev/), added as Streamlit secrets (`.streamlit/secrets.toml` locally):

```toml
GROQ_API_KEY = "your-groq-key"
SERPER_API_KEY = "your-serper-key"
```

## What this project involved

Beyond following the original tutorial concept, this build included:

- Wiring CrewAI to Groq via LiteLLM (rather than the tutorial's Hugging Face setup)
- Adding a real web search tool to eliminate hallucinated statistics
- Debugging several real-world issues: async event loop conflicts in Colab, a CrewAI caching bug incompatible with non-Anthropic providers, and Python-version/dependency conflicts during Streamlit Cloud deployment
- Deploying to Streamlit Community Cloud with secrets management (no hardcoded API keys)

## Author

Built by [Dan Shizamuayi Shina](https://github.com/shizadan) as part of an AI & Data Science learning journey — transitioning from operations/telecom retail management into applied AI.
