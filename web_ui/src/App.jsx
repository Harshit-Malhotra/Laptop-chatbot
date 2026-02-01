import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import './App.css' // We might need to ensure imports are clean, usually index.css is imported in main.jsx

function App() {
  const [messages, setMessages] = useState([
    { role: 'bot', content: "Hi! I'm your Gaming Laptop Advisor. Tell me your budget range (e.g., $1000-$1500) and I'll find the best rig for you!" }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      // Connect to the Python ADK Agent Backend
      const response = await axios.post('http://localhost:8000/chat', {
        message: input
      })

      const botMsg = {
        role: 'bot',
        content: response.data.response || "System Error: No response text."
      }
      setMessages(prev => [...prev, botMsg])
    } catch (error) {
      console.error("Error:", error)
      setMessages(prev => [...prev, {
        role: 'bot',
        content: "⚠️ Connection Error: Is the backend agent running? (port 8000)"
      }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') sendMessage()
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="status-indicator"></div>
        <div className="header-title">Adk // Gamer_Bot_v1</div>
      </div>

      <div className="messages-area">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <ReactMarkdown>{msg.content}</ReactMarkdown>
          </div>
        ))}
        {loading && (
          <div className="message bot">
            <span className="typing-dot">.</span>
            <span className="typing-dot">.</span>
            <span className="typing-dot">.</span>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-area">
        <input
          type="text"
          className="chat-input"
          placeholder="Type your budget or requirements..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyPress}
          disabled={loading}
        />
        <button onClick={sendMessage} className="send-btn" disabled={loading}>
          ➤
        </button>
      </div>
    </div>
  )
}

export default App
