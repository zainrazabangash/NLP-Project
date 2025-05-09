import grpc
import nlp_service_pb2
import nlp_service_pb2_grpc
import time
import logging
import sys

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def run():
    try:
        # Create a gRPC channel
        logger.info("Connecting to gRPC server...")
        with grpc.insecure_channel('localhost:50051') as channel:
            # Create a stub (client)
            stub = nlp_service_pb2_grpc.NLPServiceStub(channel)
            
            # Test GenerateText
            logger.info("\nTesting GenerateText...")
            try:
                response = stub.GenerateText(
                    nlp_service_pb2.TextGenerationRequest(
                        prompt="Once upon a time",
                        max_length=100,
                        try_hard=True
                    )
                )
                logger.info(f"Generated Text: {response.generated_text}")
                logger.info(f"Confidence: {response.confidence}")
                logger.info(f"Metadata: {response.metadata}")
            except grpc.RpcError as e:
                logger.error(f"Error in GenerateText: {e.details()}")
            
            # Test GetTrendingTopics
            logger.info("\nTesting GetTrendingTopics...")
            try:
                response = stub.GetTrendingTopics(
                    nlp_service_pb2.TrendingRequest(
                        country="US",
                        time_range="now 1-d"
                    )
                )
                logger.info("Trending Topics:")
                for topic in response.topics:
                    logger.info(f"- {topic}")
                logger.info(f"Timestamp: {response.timestamp}")
            except grpc.RpcError as e:
                logger.error(f"Error in GetTrendingTopics: {e.details()}")
            
            # Test GenerateStory
            logger.info("\nTesting GenerateStory...")
            try:
                response = stub.GenerateStory(
                    nlp_service_pb2.StoryRequest(
                        prompt="A magical forest",
                        max_length=200,
                        style="fairy_tale"
                    )
                )
                logger.info(f"Story: {response.story}")
                logger.info(f"Coherence Score: {response.coherence_score}")
                logger.info(f"Metadata: {response.metadata}")
            except grpc.RpcError as e:
                logger.error(f"Error in GenerateStory: {e.details()}")
            
            # Test TextToSpeech
            logger.info("\nTesting TextToSpeech...")
            try:
                response = stub.TextToSpeech(
                    nlp_service_pb2.TTSRequest(
                        text="Hello, this is a test of the text to speech service.",
                        voice="female",
                        speed=1.0
                    )
                )
                logger.info(f"Audio Format: {response.format}")
                logger.info(f"Sample Rate: {response.sample_rate}")
                logger.info(f"Audio Data Length: {len(response.audio_data)} bytes")
                
                # Save the audio file
                with open("test_audio.wav", "wb") as f:
                    f.write(response.audio_data)
                logger.info("Audio saved to test_audio.wav")
            except grpc.RpcError as e:
                logger.error(f"Error in TextToSpeech: {e.details()}")
            
            # Test StreamProcessing
            logger.info("\nTesting StreamProcessing...")
            try:
                for update in stub.StreamProcessing(
                    nlp_service_pb2.ProcessingRequest(
                        text="Test processing",
                        processing_type="markov"
                    )
                ):
                    logger.info(f"Status: {update.status}")
                    logger.info(f"Progress: {update.progress:.2%}")
                    logger.info(f"Result: {update.intermediate_result}")
                    logger.info(f"Metadata: {update.metadata}")
                    logger.info("---")
            except grpc.RpcError as e:
                logger.error(f"Error in StreamProcessing: {e.details()}")
                
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    run() 