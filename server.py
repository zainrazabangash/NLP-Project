import grpc
from concurrent import futures
import time
import nlp_service_pb2
import nlp_service_pb2_grpc
import markovify
import nltk
from TTS.api import TTS
import os
from dotenv import load_dotenv
import pandas as pd
from newsapi import NewsApiClient
import praw
from datetime import datetime, timedelta
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv("config.env")

# Initialize TTS
tts = TTS(model_name="tts_models/en/ljspeech/tacotron2-DDC", progress_bar=False, gpu=False)

# Initialize NewsAPI and Reddit clients
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY")
REDDIT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_AGENT = os.getenv("REDDIT_USER_AGENT")

logger.info("Initializing NewsAPI client...")
newsapi = NewsApiClient(api_key=NEWSAPI_KEY)

logger.info("Initializing Reddit client...")
reddit = praw.Reddit(
    client_id=REDDIT_ID,
    client_secret=REDDIT_SECRET,
    user_agent=REDDIT_AGENT
)

# Load and prepare the Markov model
def load_markov_model():
    logger.info("Loading Markov model...")
    with open("fairy_tales.txt", "r", encoding="utf-8") as f:
        text = f.read()
    start = text.find("*** START OF THE PROJECT GUTENBERG EBOOK GRIMMS' FAIRY TALES ***")
    end = text.find("*** END OF THE PROJECT GUTENBERG EBOOK GRIMMS' FAIRY TALES ***")
    corpus_gutenberg = text[start:end]
    
    # Load other corpora as needed
    # ... (your existing corpus loading code)
    
    combined_corpus = corpus_gutenberg  # Add other corpora as needed
    return markovify.Text(combined_corpus, state_size=2)

class NLPServicer(nlp_service_pb2_grpc.NLPServiceServicer):
    def __init__(self):
        logger.info("Initializing NLP Servicer...")
        self.markov_model = load_markov_model()
    
    def GenerateText(self, request, context):
        try:
            logger.info(f"Generating text with prompt: {request.prompt}")
            generated_text = self.markov_model.make_sentence(
                max_length=request.max_length,
                tries=100 if request.try_hard else 50
            )
            
            return nlp_service_pb2.TextResponse(
                generated_text=generated_text,
                confidence=0.95,
                metadata={"model": "markov", "prompt": request.prompt}
            )
        except Exception as e:
            logger.error(f"Error in GenerateText: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return nlp_service_pb2.TextResponse()
    
    def GetTrendingTopics(self, request, context):
        try:
            logger.info(f"Getting trending topics for country: {request.country}")
            topics = []
            scores = {}
            
            # Get trending topics from Reddit
            try:
                logger.info("Fetching from Reddit...")
                for submission in reddit.subreddit('all').hot(limit=5):
                    topics.append(submission.title)
                    scores[submission.title] = 1.0 - (len(topics) * 0.1)
                logger.info(f"Found {len(topics)} topics from Reddit")
            except Exception as e:
                logger.error(f"Reddit API error: {str(e)}")
            
            # Get trending topics from NewsAPI
            try:
                logger.info("Fetching from NewsAPI...")
                # Calculate date range
                end_date = datetime.now()
                start_date = end_date - timedelta(days=1)
                
                # Get top headlines
                news = newsapi.get_top_headlines(
                    language='en',
                    country=request.country.lower(),
                    from_param=start_date.strftime('%Y-%m-%d'),
                    to=end_date.strftime('%Y-%m-%d')
                )
                
                # Add news topics
                for article in news['articles'][:5]:
                    if article['title'] not in topics:
                        topics.append(article['title'])
                        scores[article['title']] = 1.0 - (len(topics) * 0.1)
                logger.info(f"Found {len(news['articles'])} articles from NewsAPI")
            except Exception as e:
                logger.error(f"NewsAPI error: {str(e)}")
            
            # If no topics were found, use defaults
            if not topics:
                logger.info("No topics found, using defaults")
                default_topics = [
                    "Technology", "Science", "Business", "Entertainment",
                    "Sports", "Health", "Politics", "Education",
                    "Environment", "Culture"
                ]
                topics = default_topics
                scores = {topic: 1.0 - (i * 0.1) for i, topic in enumerate(default_topics)}
            
            logger.info(f"Returning {len(topics)} topics")
            return nlp_service_pb2.TrendingResponse(
                topics=topics[:10],  # Limit to top 10
                scores=scores,
                timestamp=time.strftime("%Y-%m-%d %H:%M:%S")
            )
        except Exception as e:
            logger.error(f"Error in GetTrendingTopics: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return nlp_service_pb2.TrendingResponse()
    
    def GenerateStory(self, request, context):
        try:
            logger.info(f"Generating story with prompt: {request.prompt}")
            story = self.markov_model.make_sentence(
                max_length=request.max_length,
                tries=100
            )
            
            return nlp_service_pb2.StoryResponse(
                story=story,
                prompt=request.prompt,
                coherence_score=0.85,
                metadata={"style": request.style}
            )
        except Exception as e:
            logger.error(f"Error in GenerateStory: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return nlp_service_pb2.StoryResponse()
    
    def TextToSpeech(self, request, context):
        try:
            logger.info("Converting text to speech...")
            wav_path = "temp_audio.wav"
            tts.tts_to_file(
                text=request.text,
                file_path=wav_path,
                speed=request.speed
            )
            
            with open(wav_path, "rb") as f:
                audio_data = f.read()
            
            os.remove(wav_path)
            
            return nlp_service_pb2.TTSResponse(
                audio_data=audio_data,
                format="wav",
                sample_rate=22050
            )
        except Exception as e:
            logger.error(f"Error in TextToSpeech: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))
            return nlp_service_pb2.TTSResponse()
    
    def StreamProcessing(self, request, context):
        try:
            logger.info(f"Starting stream processing for type: {request.processing_type}")
            steps = ["Initializing", "Processing", "Finalizing"]
            for i, step in enumerate(steps):
                time.sleep(1)
                progress = (i + 1) / len(steps)
                logger.info(f"Processing step {i+1}/{len(steps)}: {step}")
                yield nlp_service_pb2.ProcessingUpdate(
                    status=step,
                    progress=progress,
                    intermediate_result=f"Step {i+1} completed",
                    metadata={"processing_type": request.processing_type}
                )
        except Exception as e:
            logger.error(f"Error in StreamProcessing: {str(e)}")
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(str(e))

def serve():
    logger.info("Starting gRPC server...")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nlp_service_pb2_grpc.add_NLPServiceServicer_to_server(
        NLPServicer(), server
    )
    server.add_insecure_port('[::]:50051')
    server.start()
    logger.info("NLP gRPC Server started on port 50051")
    server.wait_for_termination()

if __name__ == '__main__':
    serve() 