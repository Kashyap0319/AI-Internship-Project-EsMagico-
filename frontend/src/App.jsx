import { useState, useEffect, useRef } from 'react'
import axios from 'axios'
import { BookOpen, Send, Sparkles, Volume2, Image as ImageIcon, Mic, MicOff, Globe, Plus, Settings, Moon, Sun, Menu, X, Clock, MessageSquare } from 'lucide-react'
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
  const [sessionId, setSessionId] = useState(() => `session_${Date.now()}`)
  const [sidebarOpen, setSidebarOpen] = useState(true)
  const [darkMode, setDarkMode] = useState(false)
  const [chatHistory, setChatHistory] = useState([])
  const [currentChatTitle, setCurrentChatTitle] = useState('')
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

  // Apply dark mode class to body
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add('dark-mode')
    } else {
      document.body.classList.remove('dark-mode')
    }
  }, [darkMode])

  // Generate chat title from first message
  useEffect(() => {
    if (messages.length > 0 && !currentChatTitle) {
      const firstUserMsg = messages.find(m => m.role === 'user')
      if (firstUserMsg) {
        const title = firstUserMsg.content.slice(0, 40) + (firstUserMsg.content.length > 40 ? '...' : '')
        setCurrentChatTitle(title)
      }
    }
  }, [messages, currentChatTitle])

  const handleNewChat = () => {
    // Save current chat to history if it has messages
    if (messages.length > 0 && currentChatTitle) {
      const chatSummary = {
        id: sessionId,
        title: currentChatTitle,
        timestamp: new Date(),
        messageCount: messages.length
      }
      setChatHistory(prev => [chatSummary, ...prev.slice(0, 9)]) // Keep last 10 chats
    }

    // Reset chat state
    setMessages([])
    setSessionId(`session_${Date.now()}`)
    setCurrentChatTitle('')
    setInputValue('')
  }

  const toggleDarkMode = () => {
    setDarkMode(prev => !prev)
  }

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
        generate_audio: true,  // Enable audio narration
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

      recorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data)
        }
      }
      
      recorder.onstop = async () => {
        console.log('🎤 Recording stopped, processing...')
        const blob = new Blob(chunks, { type: 'audio/webm' })
        console.log('📦 Audio blob size:', blob.size, 'bytes')
        
        if (blob.size === 0) {
          alert('❌ No audio recorded. Please try again.')
          stream.getTracks().forEach(track => track.stop())
          return
        }
        
        const formData = new FormData()
        formData.append('audio', blob, 'recording.webm')

        try {
          setIsLoading(true)
          console.log('🚀 Sending audio for transcription...')
          
          const response = await axios.post(`${API_BASE}/transcribe`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          })
          
          console.log('✅ Transcription received:', response.data.text)
          setInputValue(response.data.text)
          setIsLoading(false)
          
          // Auto-submit after transcription
          setTimeout(() => {
            if (response.data.text && response.data.text.trim()) {
              handleSend(response.data.text)
            }
          }, 500)
          
        } catch (error) {
          console.error('❌ Transcription error:', error)
          alert('Failed to transcribe audio. Please try typing instead.')
          setIsLoading(false)
        }

        stream.getTracks().forEach(track => track.stop())
      }

      recorder.start()
      console.log('🎙️ Recording started...')
      setMediaRecorder(recorder)
      setIsRecording(true)
    } catch (error) {
      console.error('❌ Microphone access error:', error)
      alert('🎤 Microphone access denied! Please allow microphone access and try again.')
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
    <div className={`app-wrapper ${darkMode ? 'dark-mode' : ''}`}>
      {/* Sidebar */}
      <aside className={`sidebar ${sidebarOpen ? 'open' : 'closed'}`}>
        <div className="sidebar-header">
          <div className="sidebar-logo">
            <BookOpen size={24} />
            <span className="logo-text">Storytell AI</span>
          </div>
          <button className="new-chat-btn" onClick={handleNewChat}>
            <Plus size={18} />
            New Chat
          </button>
        </div>

        <div className="sidebar-content">
          <div className="knowledge-sources">
            <h3 className="sidebar-section-title">
              <Sparkles size={16} />
              Knowledge Sources
            </h3>
            <div className="source-list">
              <div className="source-item active">
                <div className="source-icon">🎩</div>
                <div className="source-info">
                  <div className="source-name">Alice in Wonderland</div>
                  <div className="source-meta">190 passages</div>
                </div>
              </div>
              <div className="source-item active">
                <div className="source-icon">⛵</div>
                <div className="source-info">
                  <div className="source-name">Gulliver's Travels</div>
                  <div className="source-meta">749 passages</div>
                </div>
              </div>
              <div className="source-item active">
                <div className="source-icon">🧞</div>
                <div className="source-info">
                  <div className="source-name">Arabian Nights</div>
                  <div className="source-meta">1224 passages</div>
                </div>
              </div>
            </div>
          </div>

          {chatHistory.length > 0 && (
            <div className="chat-history">
              <h3 className="sidebar-section-title">
                <Clock size={16} />
                Recent Chats
              </h3>
              <div className="history-list">
                {chatHistory.map((chat) => (
                  <div key={chat.id} className="history-item">
                    <MessageSquare size={14} />
                    <span>{chat.title}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        <div className="sidebar-footer">
          <button className="sidebar-action" onClick={toggleDarkMode}>
            {darkMode ? <Sun size={18} /> : <Moon size={18} />}
            <span>{darkMode ? 'Light Mode' : 'Dark Mode'}</span>
          </button>
          <button className="sidebar-action">
            <Settings size={18} />
            <span>Settings</span>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        {/* Top Bar */}
        <header className="top-bar">
          <button className="menu-toggle" onClick={() => setSidebarOpen(!sidebarOpen)}>
            {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>
          
          <div className="top-bar-title">
            <Sparkles size={20} className="title-icon" />
            <h1>Ask The Storytell AI</h1>
          </div>

          <div className="top-bar-actions">
            <div className="language-selector-compact">
              <Globe size={16} />
              <select 
                value={selectedLanguage} 
                onChange={(e) => setSelectedLanguage(e.target.value)}
                className="language-dropdown-compact"
              >
                {Object.entries(languages).map(([code, name]) => (
                  <option key={code} value={code}>{name}</option>
                ))}
              </select>
            </div>
          </div>
        </header>

        {/* Chat Area */}
        <div className="chat-area">
          <div className="messages-container">
            {messages.length === 0 && (
              <div className="welcome-message-modern">
                <div className="welcome-content">
                  <Sparkles size={56} className="welcome-icon-modern" />
                  <h2>Ask me anything about Alice, Gulliver, or Arabian adventures</h2>
                  <p className="welcome-hint-modern">Get witty answers • AI illustrations • Audio narration</p>
                  
                  {suggestions.length > 0 && (
                    <div className="welcome-suggestions">
                      {visibleSuggestions.map((suggestion, idx) => (
                        <button
                          key={idx}
                          className="suggestion-card"
                          onClick={() => handleSend(suggestion)}
                        >
                          <MessageSquare size={16} />
                          {suggestion}
                        </button>
                      ))}
                    </div>
                  )}
                </div>
              </div>
            )}

            {messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} />
            ))}

            {isLoading && (
              <div className="loading-indicator-modern">
                <div className="loading-dots">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <p>Crafting witty response...</p>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Input Area - Fixed at bottom */}
        <div className="input-area-modern">
          <div className="input-wrapper">
            <button
              onClick={isRecording ? stopRecording : startRecording}
              className={`mic-button-modern ${isRecording ? 'recording' : ''}`}
              disabled={isLoading}
              title={isRecording ? 'Stop recording' : 'Voice input'}
            >
              {isRecording ? <MicOff size={20} /> : <Mic size={20} />}
            </button>
            
            <input
              type="text"
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about Alice, Gulliver, or Arabian adventures..."
              disabled={isLoading}
              className="chat-input-modern"
            />
            
            <button
              onClick={() => handleSend()}
              disabled={!inputValue.trim() || isLoading}
              className="send-button-modern"
              title="Send message"
            >
              <Send size={20} />
            </button>
          </div>
        </div>
      </main>
    </div>
  )
}

export default App
