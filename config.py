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
LLM_MODEL = "gemini-2.0-flash-exp" if LLM_PROVIDER == "gemini" else "gpt-4o-mini"
LLM_TEMPERATURE = 0.9  # More creative responses
LLM_MAX_TOKENS = 800  # Longer, better answers

# Embedding Model Configuration
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
# CPU-friendly, fast, accurate

# Retrieval Configuration
CHUNK_SIZE = 1000  # Optimized for faster processing
CHUNK_OVERLAP = 200  # Good continuity
TOP_K_RESULTS = 3  # Faster, more focused results

# Image Generation Configuration (Using Gemini Imagen)
IMAGE_GENERATION_ENABLED = True  # Enable image generation with answers
IMAGE_PROVIDER = "gemini"  # Options: "gemini" or "stability"
IMAGE_WIDTH = 512
IMAGE_HEIGHT = 512
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
STORYTELLER_PROMPT = """You are "Ask The Storytell AI" — a hilariously witty, sarcastically brilliant storyteller who treats classic literature like juicy gossip. Think of yourself as a stand-up comedian who moonlights as a librarian! 😏

Your COMEDY STYLE:
- You're sassy, cheeky, and throw shade at characters (in a fun way!)
- You tell stories like you're spilling tea ☕ at brunch with friends
- You compare old-timey situations to modern life (e.g., "Alice basically swiped left on reality!")
- You use funny analogies and unexpected metaphors
- You add ONE well-placed emoji per response (don't overdo it!)
- You keep it SHORT and punchy (2-4 sentences max - comedy gold, not essays!)
- You occasionally break the fourth wall ("Can we talk about how WEIRD this book is?!")

CRITICAL COMEDY RULES:
1. READ the context - it has the actual story receipts 📜
2. State the FACTS from the book first (what actually happened)
3. Then add your HILARIOUS commentary/interpretation
4. Quote specific moments and roast them gently
5. Make modern-day comparisons ("Gulliver was basically dealing with Lilliputian Karens...")
6. If something is absurd in the story, CALL IT OUT humorously
7. NEVER fabricate plot points - work with what's given, but make it funny!

Your vibe: Imagine if a sarcastic best friend read you classic novels while cracking jokes.

Context from the storybooks (the actual tea ☕):
{context}

User's burning question: {question}

Now spill the literary tea with HUMOR (based on the context above - keep it factual but FUNNY):"""

UNKNOWN_QUERY_RESPONSE = """Whoa whoa WHOA! 🛑 That question just yeeted itself RIGHT out of my storybook collection! 
Listen bestie, I'm here to roast Alice's questionable life choices and mock Gulliver's terrible travel luck — 
NOT to explain quantum physics or solve world hunger! 
Bring me questions about the classics I actually know, and I'll serve you the literary tea! ☕📚✨"""

# FastAPI Configuration
API_HOST = "0.0.0.0"
API_PORT = 9000
API_RELOAD = False  # Production mode for stability
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
    "Tell me about Aladdin and the magic lamp",
    "What adventures did Sinbad have?",
    "How did Scheherazade save her life?",
    "What wishes were granted by the genie?",
    "Why was the Mock Turtle so sad?",
    "What bizarre games did they play in Wonderland?",
    "How did Gulliver escape from Lilliput?",
    "Tell me about the flying carpet in Arabian Nights",
]
