import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { BookOpen, Send, Sparkles, Volume2, Image as ImageIcon, Mic, MicOff, Globe } from 'lucide-react'
import './App.css'
import ChatMessage from './components/ChatMessage'
import SuggestionPill from './components/SuggestionPill'

const API_BASE = '/api'

function App() {
  const [messages, setMessages] = useState([])
  const [inputValue, setInputValue] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [suggestions, setSuggestions] = useState([])
  const [currentSuggestionIndex, setCurrentSuggestionIndex] = useState(0)
  const [languages, setLanguages] = useState({})
  const [selectedLanguage, setSelectedLanguage] = useState('en')
  const [isRecording, setIsRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState(null)
  const [sessionId] = useState(() => `session_${Date.now()}`)
  const messagesEndRef = useRef(null)

  // Fetch suggestions and languages on mount
  useEffect(() => {
    axios.get(`${API_BASE}/suggestions`)
      .then(res => setSuggestions(res.data.suggestions))
      .catch(err => console.error('Error fetching suggestions:', err))
    
    axios.get(`${API_BASE}/languages`)
      .then(res => setLanguages(res.data.languages))
      .catch(err => console.error('Error fetching languages:', err))
  }, [])

  // Rotate suggestions every 5 seconds
  useEffect(() => {
    if (suggestions.length === 0) return
    
    const interval = setInterval(() => {
      setCurrentSuggestionIndex((prev) => (prev + 1) % suggestions.length)
    }, 5000)
    
    return () => clearInterval(interval)
  }, [suggestions])

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async (question = null) => {
    const textToSend = question || inputValue.trim()
    
    if (!textToSend || isLoading) return

    // Add user message
    const userMessage = {
      role: 'user',
      content: textToSend,
      timestamp: new Date()
    }
    
    setMessages(prev => [...prev, userMessage])
    setInputValue('')
    setIsLoading(true)

    try {
      const response = await axios.post(`${API_BASE}/chat`, {
        question: textToSend,
        generate_image: true,  // Always generate images
        generate_audio: true,
        language: selectedLanguage,
        session_id: sessionId
      })

      const botMessage = {
        role: 'assistant',
        content: response.data.answer,
        imageUrl: response.data.image_url,
        audioUrl: response.data.audio_url,
        sources: response.data.sources,
        timestamp: new Date()
      }

      setMessages(prev => [...prev, botMessage])
    } catch (error) {
      console.error('Error:', error)
      
      const errorMessage = {
        role: 'assistant',
        content: '😅 Oops! Something went wrong. Please try again!',
        timestamp: new Date()
      }
      
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)
      const chunks = []

      recorder.ondataavailable = (e) => chunks.push(e.data)
      
      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' })
        const formData = new FormData()
        formData.append('audio', blob, 'recording.webm')

        try {
          setIsLoading(true)
          const response = await axios.post(`${API_BASE}/transcribe`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          
          setInputValue(response.data.text)
          setIsLoading(false)
        } catch (error) {
          console.error('Transcription error:', error)
          setIsLoading(false)
        }

        stream.getTracks().forEach(track => track.stop())
      }

      recorder.start()
      setMediaRecorder(recorder)
      setIsRecording(true)
    } catch (error) {
      console.error('Microphone access error:', error)
      alert('Microphone access denied or not available')
    }
  }

  const stopRecording = () => {
    if (mediaRecorder && isRecording) {
      mediaRecorder.stop()
      setIsRecording(false)
      setMediaRecorder(null)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const visibleSuggestions = suggestions.slice(currentSuggestionIndex, currentSuggestionIndex + 3)
  if (visibleSuggestions.length < 3 && suggestions.length >= 3) {
    visibleSuggestions.push(...suggestions.slice(0, 3 - visibleSuggestions.length))
  }

  return (
    <div className="app-container">
      <div className="chat-container">
        {/* Header */}
        <div className="chat-header">
          <div className="header-content">
            <BookOpen className="header-icon" size={32} />
            <div>
              <h1 className="header-title">Ask The Storytell AI</h1>
              <p className="header-subtitle">Witty tales from classic storybooks 📚✨</p>
            </div>
          </div>
        </div>

        {/* Book Showcase */}
        <div className="books-showcase">
          <p className="books-title">📖 Featured Story Collection</p>
          <div className="books-grid">
            <div className="book-card">
              <div className="book-cover-wrapper">
                <img 
                  src="https://www.gutenberg.org/cache/epub/11/pg11.cover.medium.jpg" 
                  alt="Alice in Wonderland"
                  className="book-cover-image"
                  onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
                />
                <div className="book-cover alice fallback">🎩</div>
              </div>
              <p className="book-title">Alice in Wonderland</p>
            </div>
            <div className="book-card">
              <div className="book-cover-wrapper">
                <img 
                  src="https://www.gutenberg.org/cache/epub/829/pg829.cover.medium.jpg" 
                  alt="Gulliver's Travels"
                  className="book-cover-image"
                  onError={(e) => { e.target.style.display = 'none'; e.target.nextSibling.style.display = 'flex'; }}
                />
                <div className="book-cover gulliver fallback">⛵</div>
              </div>
              <p className="book-title">Gulliver's Travels</p>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="messages-area">
          {messages.length === 0 && (
            <div className="welcome-message">
              <Sparkles size={48} className="welcome-icon" />
              <h2>Welcome to the Storytelling Universe!</h2>
              <p>Ask me anything about classic tales like Alice in Wonderland or Gulliver's Travels.</p>
              <p className="welcome-hint">I'll reply with witty commentary, beautiful illustrations, and even narrate the story! 🎭</p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <ChatMessage key={idx} message={msg} />
          ))}

          {isLoading && (
            <div className="loading-indicator">
              <div className="loading-dots">
                <span></span>
                <span></span>
                <span></span>
              </div>
              <p>Crafting a witty response...</p>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Suggestions */}
        {messages.length === 0 && suggestions.length > 0 && (
          <div className="suggestions-container">
            <p className="suggestions-label">Try asking:</p>
            <div className="suggestions-pills">
              {visibleSuggestions.map((suggestion, idx) => (
                <SuggestionPill 
                  key={idx} 
                  text={suggestion}
                  onClick={() => handleSend(suggestion)}
                />
              ))}
            </div>
          </div>
        )}

        {/* Input Area */}
        <div className="input-area">
          <div className="input-container">
            {/* Language Selector */}
            <div className="language-selector">
              <Globe size={16} />
              <select 
                value={selectedLanguage} 
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="language-dropdown"
              >
                {Object.entries(languages).map(([code, name]) => (
                  <option key={code} value={code}>{name}</option>
                ))}
              </select>
            </div>
            
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the stories..."
              disabled={isLoading}
              className="chat-input"
            />
            
            {/* Mic Button */}
            <button
              onClick={isRecording ? stopRecording : startRecording}
              className={`mic-button ${isRecording ? 'recording' : ''}`}
              disabled={isLoading}
              title={isRecording ? 'Stop recording' : 'Voice input'}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </button>
            
            <button
              onClick={() => handleSend()}
              disabled={!inputValue.trim() || isLoading}
              className="send-button"
            >
              <Send size={20} />
            </button>
          </div>
          <div className="input-footer">
            <span className="feature-badge">
              <Sparkles size={14} /> AI Illustrations
            </span>
            <span className="feature-badge">
              <Volume2 size={14} /> Audio Narration
            </span>
            <span className="feature-badge">
              <Mic size={14} /> Voice Input
            </span>
            <span className="feature-badge">
              <Globe size={14} /> Multi-lingual
            </span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
