"""
Configuration file for Ask The Storytell AI
Allows easy switching between different models and settings
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Project Paths
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
PDF_DIR = DATA_DIR / "pdfs"
STATIC_DIR = BASE_DIR / "static"
IMAGES_DIR = STATIC_DIR / "images"
AUDIO_DIR = STATIC_DIR / "audio"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
PDF_DIR.mkdir(exist_ok=True)
STATIC_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)
AUDIO_DIR.mkdir(exist_ok=True)

# API Keys (from environment variables)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
STABILITY_API_KEY = os.getenv("STABILITY_API_KEY", "")
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "gemini")  # Options: "gemini" or "openai"
LLM_MODEL = "gemini-2.0-flash" if LLM_PROVIDER == "gemini" else "gpt-4o-mini"
LLM_TEMPERATURE = 0.8
LLM_MAX_TOKENS = 512

# Embedding Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# CPU-friendly, fast, accurate

# Retrieval Configuration
CHUNK_SIZE = 1200  # Balanced size for context vs memory
CHUNK_OVERLAP = 250  # Good continuity without excessive overlap
TOP_K_RESULTS = 5  # Number of relevant chunks to retrieve (used as default)

# Image Generation Configuration (Stability AI)
IMAGE_GENERATION_ENABLED = True
STABILITY_API_URL = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
IMAGE_WIDTH = 1024
IMAGE_HEIGHT = 1024
IMAGE_STEPS = 30
IMAGE_STYLE = "fantasy-art"  # For storybook-style images

# Audio Configuration (ElevenLabs)
AUDIO_ENABLED = True
ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_VOICE_ID = "21m00Tcm4TlvDq8ikWAM"  # Rachel - warm storyteller voice
# Other options: "EXAVITQu4vr4xnSDxMaL" (Bella), "ErXwobaYiN019PkySvjV" (Antoni)
AUDIO_STABILITY = 0.5
AUDIO_SIMILARITY_BOOST = 0.75

# Storyteller Persona Configuration
STORYTELLER_NAME = "Ask The Storytell AI"
STORYTELLER_PROMPT = """You are "Ask The Storytell AI" — a witty, sarcastic, and highly entertaining storyteller who is an EXPERT on classic literature.

Your personality:
- You're clever, sarcastic, and love adding humorous commentary
- You tell stories with dramatic flair and comedic timing
- You use emojis sparingly but effectively
- You stay STRICTLY grounded in the actual story content provided in the context
- You keep answers concise (2-4 sentences max)
- You NEVER make up information - you ONLY use what's in the context below

CRITICAL RULES:
1. READ the context carefully - it contains actual excerpts from the books
2. Answer ONLY based on what is explicitly stated in the context
3. Quote specific details, character names, and events from the context
4. If the context mentions a specific scene or dialogue, reference it directly
5. Add your witty commentary AFTER stating the facts from the book
6. If the context doesn't contain enough information, say so humorously

Context from the storybooks:
{context}

User's question: {question}

Respond as the witty storyteller (USE THE CONTEXT ABOVE - don't make things up):"""

UNKNOWN_QUERY_RESPONSE = """Whoa, hold up! 🤚 That's not in my storybook collection. 
I'm here to dish out tales about Alice's rabbit-hole adventures and Gulliver's giant problems — 
not to solve the mysteries of the universe! Try asking me something from the classic stories I actually know! 📚✨"""

# FastAPI Configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_RELOAD = True  # Set to False in production
# Allow all origins during development to avoid port-mismatch issues
CORS_ORIGINS = ["*"]

# Multi-language Support
SUPPORTED_LANGUAGES = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "hi": "Hindi",
    "ar": "Arabic",
    "zh": "Chinese",
    "ja": "Japanese"
}

# Conversation Memory
MAX_CONVERSATION_HISTORY = 10  # Max messages to keep in memory

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FILE = BASE_DIR / "storytell_ai.log"

# Suggested Questions for Frontend
SUGGESTED_QUESTIONS = [
    "What was the weirdest moment at the Mad Hatter's tea party?",
    "Tell me about Alice's encounter with the Cheshire Cat",
    "What happened when Gulliver woke up in Lilliput?",
    "How did Alice change sizes in Wonderland?",
    "What was the Queen of Hearts obsessed with?",
    "Describe Gulliver's visit to the land of giants",
    "What did the Caterpillar tell Alice?",
    "Why was the Mock Turtle so sad?",
    "What bizarre games did they play in Wonderland?",
    "How did Gulliver escape from Lilliput?",
]
