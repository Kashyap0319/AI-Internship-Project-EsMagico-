# Story Chat Interface - Quick Start Guide

## 🎯 What This Does

Ask questions about classic stories (Alice in Wonderland, Gulliver's Travels) and get:
- 🎭 Funny, entertaining answers
- 🎨 AI-generated illustrations
- 🔊 Audio responses (optional)
- 🌍 Multi-language support

## ⚡ Quick Start (5 Minutes)

### 1. Install Prerequisites
```powershell
# Install Python 3.9+ from python.org
# Install Ollama from ollama.ai

# Verify installations
python --version
ollama --version
```

### 2. Setup Project
```powershell
# Navigate to project
cd "c:\Users\Shrey\OneDrive\Desktop\Day 2 Ai Project"

# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\activate

# Run setup
python setup.py
```

### 3. Install Ollama Model
```powershell
# Pull the LLM (one-time, ~2GB)
ollama pull llama3.2

# Start Ollama server
ollama serve
```

### 4. Add Your PDFs
```powershell
# Copy your story PDFs to data/pdfs/
# For example:
copy "c:\Users\Shrey\OneDrive\Desktop\Alice_In_Wonderland.pdf" "data\pdfs\"
copy "c:\Users\Shrey\OneDrive\Desktop\Gullivers_Travels.pdf" "data\pdfs\"
```

### 5. Run the App
```powershell
python main.py
```

### 6. Open in Browser
Navigate to: **http://localhost:7860**

## 🎮 How to Use

1. **Type a question** about the stories
   - Example: "Tell me about Alice's adventures"
   
2. **Or record audio** using the microphone button

3. **Click "Ask the Storyteller"**

4. **View**:
   - Funny text response
   - AI-generated image
   - Audio playback (if enabled)
   - Source citations

## 🔧 Troubleshooting

### "Ollama connection failed"
```powershell
# Start Ollama in a new terminal
ollama serve
```

### "No module named X"
```powershell
# Ensure venv is activated
.\venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

### "No PDF files found"
```powershell
# Add PDFs to data/pdfs/
copy "path\to\your\story.pdf" "data\pdfs\"
```

### Slow image generation
```python
# In config.py, disable or reduce quality:
IMAGE_GENERATION_ENABLED = False  # Disable
# OR
IMAGE_STEPS = 15  # Faster, lower quality
```

## 📝 Example Questions

- "Who is Alice?"
- "Tell me about the Mad Hatter's tea party"
- "What happened when Gulliver visited Lilliput?"
- "Describe the Queen of Hearts"
- "What did the Cheshire Cat say?"

Try asking something unrelated to see the funny fallback responses! 😄

## 🎯 Key Features

| Feature | Status | Details |
|---------|--------|---------|
| Text Q&A | ✅ | RAG-based answers from PDFs |
| Funny Tone | ✅ | Humorous, entertaining responses |
| Image Gen | ✅ | Stable Diffusion illustrations |
| Audio Input | ✅ | Whisper speech-to-text |
| Audio Output | ✅ | gTTS text-to-speech |
| Multi-lingual | ✅ | 8 languages supported |
| Follow-ups | ✅ | Conversation memory |

## 🔄 Configuration

Edit `config.py` to customize:

```python
# Disable features for faster testing
IMAGE_GENERATION_ENABLED = False
AUDIO_INPUT_ENABLED = False
AUDIO_OUTPUT_ENABLED = False

# Change models
LLM_MODEL = "mistral"  # Smaller, faster
WHISPER_MODEL = "tiny"  # Faster transcription
```

## 📚 Next Steps

1. Read **README.md** for full documentation
2. Check **config.py** for all options
3. Review logs in **story_chat.log**
4. Explore the code modules

## 🆘 Need Help?

1. Check `story_chat.log` for errors
2. Verify Ollama is running: `ollama list`
3. Ensure PDFs are in `data/pdfs/`
4. Try disabling image generation for faster testing

---

**Have fun chatting with classic stories! 📚✨**
