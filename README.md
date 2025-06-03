# TrendStory

**Offline trend-driven story generator**  
Fetch real-time trends (NewsAPI, Reddit, Google Trends), stitch them into short narratives with a local Markov chain trained on multiple corpora, then render them to speech—all inside a Jupyter Notebook and Docker container.

---

### 📊 Trend Analysis
- **Multiple Data Sources**
  - NewsAPI integration for real-time news headlines
  - Reddit API for trending discussions and topics
  - Google Trends data for popular search queries

### 📚 Story Generation
- **Rich Training Data**
  - Grimm's Fairy Tales (Project Gutenberg)  
  - Kaggle Writing Prompts  
  - ChatGPT-4o Writing Prompts  
- **Advanced Text Generation**
  - Markov chain-based story generation
  - Multi-corpus training for diverse narratives
- **Story Enhancement** 
  - `state_size=2` Markovify chains  
  - Optional topic-biased submodel for trend relevance

### 🔊 Audio Output
- **High-Quality Text-to-Speech**
  - Coqui TTS integration
  - "ljspeech/tacotron2-DDC" model
  - Natural-sounding voice synthesis

### 💻 User Interface
- **Interactive Development**
  - Jupyter Notebook integration
  - Real-time code execution
- **Web Interface**
  - Gradio-based user interface
  - Real-time story generation

### 🐳 Deployment
- **Containerized Solution**
  - Docker support with Python 3.11
  - Jupyter server on port 8888
  - Gradio server on port 7860
- **Easy Setup**
  - Simple pip installation
  - Environment variable configuration

## 🛠️ Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/TrendStory.git
cd TrendStory
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
- Copy `config.env.example` to `config.env`
- Add your API keys and configuration

4. Run with Docker:
```bash
docker build -t trendstory .
docker run -p 8888:8888 -p 7860:7860 trendstory
```

## 📝 Usage

1. Start the server:
```bash
python server.py
```

2. Run the client:
```bash
python client.py
```

3. Access the Gradio UI at `http://localhost:7860`

## 🔮 Future Improvements

- [ ] Replace Markovify model with a fine-tuned language model for better story coherence and creativity
- [ ] Implement better trend analysis and topic clustering
- [ ] Add more diverse training corpora
- [ ] Improve story structure and narrative flow
- [ ] Add support for multiple languages

## 🙏 Acknowledgments

- Project Gutenberg for the fairy tales corpus
- Kaggle Writing Prompts dataset
- Coqui TTS for the text-to-speech model

