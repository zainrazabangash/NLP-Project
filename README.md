# TrendStory

**Offline trend-driven story generator**  
Fetch real-time trends (NewsAPI, Reddit, Google Trends), stitch them into short narratives with a local Markov chain trained on multiple corpora, then render them to speech—all inside a Jupyter Notebook and Docker container.

---

## 🚀 Features

- **Live Trend Sources**  
  - NewsAPI top headlines (`NEWSAPI_KEY`)  
  - Reddit hot posts (`praw`)  
  - Google Trends via `pytrends`  
- **Multi-Corpus Markov Model**  
  - Grimm’s Fairy Tales (Project Gutenberg)  
  - Kaggle Writing Prompts  
  - ChatGPT-4o Writing Prompts  
- **Enhanced Coherence**  
  - `state_size=2` Markovify chains  
  - Optional topic-biased submodel for trend relevance
- **Offline TTS**  
  - Coqui TTS “ljspeech/tacotron2-DDC” model  
- **Interactive UI**  
  - Jupyter Notebook for exploration  
  - Gradio UI
- **Containerized**  
  - Dockerfile boots Jupyter on port 8888  
  - Mount your code for live editing

