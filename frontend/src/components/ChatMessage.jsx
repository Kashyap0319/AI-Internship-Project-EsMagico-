import { Volume2, Image as ImageIcon, BookOpen } from 'lucide-react'
import { useState, useRef, useEffect } from 'react'
import './ChatMessage.css'

function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  const [isPlaying, setIsPlaying] = useState(false)
  const audioRef = useRef(null)

  useEffect(() => {
    // Auto-play audio when message appears
    if (message.audioUrl && audioRef.current) {
      audioRef.current.play().catch(err => console.log('Autoplay prevented:', err))
    }
  }, [message.audioUrl])

  const handleAudioPlay = () => {
    if (audioRef.current) {
      if (isPlaying) {
        audioRef.current.pause()
      } else {
        audioRef.current.play()
      }
    }
  }

  return (
    <div className={`message ${isUser ? 'user-message' : 'bot-message'}`}>
      <div className="message-content">
        {!isUser && (
          <div className="bot-avatar">
            <BookOpen size={20} />
          </div>
        )}
        
        <div className="message-bubble">
          <p className="message-text">{message.content}</p>
          
          {message.imageUrl && (
            <div className="message-image">
              <img src={message.imageUrl} alt="Story illustration" />
              <div className="image-badge">
                <ImageIcon size={14} /> AI Generated
              </div>
            </div>
          )}
          
          {message.audioUrl && (
            <div className="message-audio">
              <audio 
                ref={audioRef} 
                src={message.audioUrl}
                onPlay={() => setIsPlaying(true)}
                onPause={() => setIsPlaying(false)}
                onEnded={() => setIsPlaying(false)}
              />
              <button 
                className="audio-button"
                onClick={handleAudioPlay}
              >
                <Volume2 size={16} />
                {isPlaying ? 'Pause Narration' : 'Play Narration'}
              </button>
            </div>
          )}
          
          {message.sources && message.sources.length > 0 && (
            <details className="message-sources">
              <summary>📚 Sources ({message.sources.length})</summary>
              <div className="sources-list">
                {message.sources.map((source, idx) => (
                  <div key={idx} className="source-item">
                    <div className="source-header">
                      <span className="source-name">{source.source}</span>
                      <span className="source-score">Score: {source.score}</span>
                    </div>
                    <p className="source-text">{source.text}</p>
                  </div>
                ))}
              </div>
            </details>
          )}
        </div>
        
        {isUser && (
          <div className="user-avatar">
            <span>You</span>
          </div>
        )}
      </div>
      
      <div className="message-timestamp">
        {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
      </div>
    </div>
  )
}

export default ChatMessage
