import React, { useState, useRef, useEffect } from 'react'
import { Bold, Italic, Strikethrough, Paperclip, Smile, AtSign, ChevronUp } from 'lucide-react'
import api from '../api/axios'
import '../styles/MessageInput.css'

export default function MessageInput({ channelId, channelName, onSent }){
  const [text, setText] = useState('')
  const textareaRef = useRef(null)
  
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = textareaRef.current.scrollHeight + 'px'
    }
  }, [text])

  const send = async () => {
    if(!text.trim()) return
    try{
      const payload = { channel_id: Number(channelId), user_id: 1, content: text }
      await api.post('/messages/', payload)
      setText('')
      if(onSent) onSent()
    }catch(e){
      console.error(e)
    }
  }

  const handleKeyDown = (e) => {
    if(e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      send()
    }
  }

  return (
    <div className="message-input-container">
      <div className="message-input-wrapper">
        <textarea 
          ref={textareaRef}
          value={text} 
          onChange={e=>setText(e.target.value)}
          onKeyDown={handleKeyDown}
          className="message-input"
          placeholder={`Message #${channelName || 'channel'}`}
          rows={1}
        />
        <div className="message-input-toolbar">
          <div className="message-input-icons">
            <div className="message-input-formatting">
              <button className="message-input-icon" title="Bold" aria-label="Bold">
                <Bold size={16} />
              </button>
              <button className="message-input-icon" title="Italic" aria-label="Italic">
                <Italic size={16} />
              </button>
              <button className="message-input-icon" title="Strikethrough" aria-label="Strikethrough">
                <Strikethrough size={16} />
              </button>
            </div>
            <button className="message-input-icon message-input-attach" title="Attach file" aria-label="Attach">
              <Paperclip size={16} />
            </button>
            <button className="message-input-icon message-input-emoji" title="Emoji" aria-label="Add emoji">
              <Smile size={16} />
            </button>
            <button className="message-input-icon message-input-mention" title="Mention" aria-label="Mention">
              <AtSign size={16} />
            </button>
          </div>
          <div className="message-input-actions">
            <button 
              onClick={send} 
              className="send-button"
              disabled={!text.trim()}
              title="Send message"
              aria-label="Send"
            >
              <ChevronUp size={16} />
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
