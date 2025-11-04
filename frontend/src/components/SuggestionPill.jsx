import { Sparkles } from 'lucide-react'
import './SuggestionPill.css'

function SuggestionPill({ text, onClick }) {
  return (
    <button className="suggestion-pill" onClick={onClick}>
      <Sparkles size={14} className="pill-icon" />
      <span className="pill-text">{text}</span>
    </button>
  )
}

export default SuggestionPill
