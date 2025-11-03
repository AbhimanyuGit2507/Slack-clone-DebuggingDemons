import React, { useState, useRef, useEffect } from 'react'
import api from '../api/axios'
import '../styles/RichTextComposer.css'

export default function RichTextComposer({ channelId, dmUserId, channelName, onSent }) {
  const [content, setContent] = useState('')
  const [showFormatting, setShowFormatting] = useState(true)
  const [showEmojiPicker, setShowEmojiPicker] = useState(false)
  const [showMentionPicker, setShowMentionPicker] = useState(false)
  const [mentionPickerPosition, setMentionPickerPosition] = useState({ top: 0, left: 0 })
  const [selectedFiles, setSelectedFiles] = useState([])
  const [contacts, setContacts] = useState([])
  const editorRef = useRef(null)
  const fileInputRef = useRef(null)
  const mentionPickerRef = useRef(null)

  const isDM = !!dmUserId

  // Fetch users for mentions
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        // Fetch all users from the database
        const res = await api.get('/api/users')
        const allUsers = res.data.map(user => ({
          id: user.id,
          name: user.full_name || user.name || user.username,
          username: user.username,
          profile_picture: user.profile_picture || user.avatar_url || null
        }))
        
        // If in DM, prioritize showing current user and DM recipient first
        if (isDM && dmUserId) {
          const dmUser = allUsers.find(u => u.id === parseInt(dmUserId))
          const currentUser = allUsers.find(u => u.id === 2) // Assuming current user ID is 2
          const otherUsers = allUsers.filter(u => u.id !== parseInt(dmUserId) && u.id !== 2)
          
          setContacts([
            ...(currentUser ? [{ ...currentUser, name: currentUser.name + ' (you)' }] : []),
            ...(dmUser ? [dmUser] : []),
            ...otherUsers
          ])
        } else {
          setContacts(allUsers)
        }
      } catch (err) {
        console.error('Error fetching users:', err)
        // Fallback to mock data
        setContacts([
          { id: 1, name: 'Harsh Paliwal', username: 'harsh', profile_picture: null },
          { id: 2, name: 'Abhimanyu Negi (you)', username: 'abhimanyu', profile_picture: null }
        ])
      }
    }
    fetchUsers()
  }, [channelId, dmUserId, isDM])

  // Apply formatting to selected text
  const applyFormat = (format) => {
    const editor = editorRef.current
    if (!editor) return

    editor.focus()
    const selection = window.getSelection()
    
    if (selection.rangeCount === 0) return

    const range = selection.getRangeAt(0)
    
    switch (format) {
      case 'bold':
        document.execCommand('bold', false, null)
        break
      case 'italic':
        document.execCommand('italic', false, null)
        break
      case 'underline':
        document.execCommand('underline', false, null)
        break
      case 'strikethrough':
        document.execCommand('strikeThrough', false, null)
        break
      case 'link':
        const url = prompt('Enter URL:')
        if (url) document.execCommand('createLink', false, url)
        break
      case 'orderedList':
        document.execCommand('insertOrderedList', false, null)
        break
      case 'unorderedList':
        document.execCommand('insertUnorderedList', false, null)
        break
      case 'blockquote':
        document.execCommand('formatBlock', false, 'blockquote')
        break
      case 'code':
        const code = document.createElement('code')
        range.surroundContents(code)
        break
      case 'codeBlock':
        const pre = document.createElement('pre')
        const codeBlock = document.createElement('code')
        codeBlock.textContent = selection.toString()
        pre.appendChild(codeBlock)
        range.deleteContents()
        range.insertNode(pre)
        break
      default:
        break
    }

    // Update content
    setContent(editor.innerHTML)
  }

  // Handle file selection
  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files)
    setSelectedFiles(prev => [...prev, ...files])
  }

  // Remove selected file
  const removeFile = (index) => {
    setSelectedFiles(prev => prev.filter((_, i) => i !== index))
  }

  // Insert emoji
  const insertEmoji = (emoji) => {
    const editor = editorRef.current
    if (editor) {
      editor.focus()
      document.execCommand('insertText', false, emoji)
      setContent(editor.innerHTML)
    }
    setShowEmojiPicker(false)
  }

  // Common emojis
  const commonEmojis = ['😀', '😂', '❤️', '👍', '👏', '🎉', '🔥', '✨', '💯', '🚀', '👀', '🤔', '😊', '😎', '💪']

  // Show mention picker at cursor position
  const showMentionPickerAtCursor = () => {
    const editor = editorRef.current
    if (!editor) return

    editor.focus()
    
    // Insert @ symbol at cursor
    document.execCommand('insertText', false, '@')
    
    // Get cursor position
    const selection = window.getSelection()
    if (selection.rangeCount > 0) {
      const range = selection.getRangeAt(0)
      const rect = range.getBoundingClientRect()
      const editorRect = editor.getBoundingClientRect()
      
      // Position popup above the @ symbol, closer to text
      setMentionPickerPosition({
        top: rect.top - 215, // Position above (adjusted for closer placement)
        left: rect.left
      })
      setShowMentionPicker(true)
    }
  }

  // Close mention picker on Esc key
  useEffect(() => {
    const handleEscape = (e) => {
      if (e.key === 'Escape' && showMentionPicker) {
        e.preventDefault()
        setShowMentionPicker(false)
        editorRef.current?.focus()
      }
    }
    
    if (showMentionPicker) {
      document.addEventListener('keydown', handleEscape)
    }
    
    return () => {
      document.removeEventListener('keydown', handleEscape)
    }
  }, [showMentionPicker])

  // Insert mention
  const insertMention = (contact) => {
    const editor = editorRef.current
    if (!editor) return
    
    editor.focus()
    
    // Find and remove the @ symbol from the content
    const html = editor.innerHTML
    const lastAtIndex = html.lastIndexOf('@')
    
    if (lastAtIndex !== -1) {
      // Remove the @ character
      editor.innerHTML = html.substring(0, lastAtIndex) + html.substring(lastAtIndex + 1)
    }
    
    // Get current selection
    const selection = window.getSelection()
    const range = document.createRange()
    
    // Find the last text node to insert mention
    const walker = document.createTreeWalker(
      editor,
      NodeFilter.SHOW_TEXT,
      null,
      false
    )
    
    let lastTextNode = null
    while (walker.nextNode()) {
      lastTextNode = walker.currentNode
    }
    
    // Create mention span with blue color
    const mention = document.createElement('span')
    mention.className = 'mention'
    mention.contentEditable = 'false'
    mention.textContent = `@${contact.name}`
    mention.setAttribute('data-user-id', contact.id)
    mention.setAttribute('data-username', contact.username)
    mention.style.color = '#1d9bd1'
    mention.style.cursor = 'pointer'
    mention.style.fontWeight = '500'
    
    // Add space after mention
    const space = document.createTextNode('\u00A0')
    
    if (lastTextNode && lastTextNode.parentNode) {
      // Insert after the last text node
      lastTextNode.parentNode.appendChild(mention)
      lastTextNode.parentNode.appendChild(space)
    } else {
      // If no text node, append to editor
      editor.appendChild(mention)
      editor.appendChild(space)
    }
    
    // Move cursor after the space
    range.setStartAfter(space)
    range.setEndAfter(space)
    selection.removeAllRanges()
    selection.addRange(range)
    
    setContent(editor.innerHTML)
    setShowMentionPicker(false)
  }

  // Close mention picker when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (mentionPickerRef.current && !mentionPickerRef.current.contains(event.target)) {
        setShowMentionPicker(false)
      }
    }
    
    if (showMentionPicker) {
      document.addEventListener('mousedown', handleClickOutside)
    }
    
    return () => {
      document.removeEventListener('mousedown', handleClickOutside)
    }
  }, [showMentionPicker])

  // Send message
  const send = async () => {
    const editor = editorRef.current
    if (!editor || (!editor.innerText.trim() && selectedFiles.length === 0)) return

    try {
      const formData = new FormData()
      
      // Add message content
      const htmlContent = editor.innerHTML
      const plainText = editor.innerText
      
      // Debug: log the HTML content
      console.log('Sending HTML:', htmlContent)
      console.log('Sending plain text:', plainText)
      
      if (isDM) {
        formData.append('receiver_id', dmUserId)
        formData.append('content', plainText)
        formData.append('formatted_content', htmlContent)
      } else {
        formData.append('channel_id', channelId)
        formData.append('user_id', 1) // TODO: Get from auth context
        formData.append('content', plainText)
        formData.append('formatted_content', htmlContent)
      }

      // Add files
      selectedFiles.forEach((file, index) => {
        formData.append('files', file)
      })

      // Send to backend
      const endpoint = isDM ? '/api/direct-messages/' : '/api/messages/'
      await api.post(endpoint, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      // Clear editor
      editor.innerHTML = ''
      setContent('')
      setSelectedFiles([])
      
      if (onSent) onSent()
    } catch (e) {
      console.error('Error sending message:', e)
    }
  }

  // Handle keyboard shortcuts
  const handleKeyDown = (e) => {
    // Check if cursor is inside a list
    const selection = window.getSelection()
    const node = selection.anchorNode
    let isInList = false
    let listItem = null
    
    // Check if we're inside a list element
    if (node) {
      let parent = node.nodeType === 3 ? node.parentElement : node
      while (parent && parent !== editorRef.current) {
        if (parent.tagName === 'LI') {
          isInList = true
          listItem = parent
          break
        }
        parent = parent.parentElement
      }
    }
    
    // Handle Enter key
    if (e.key === 'Enter') {
      if (e.shiftKey && isInList) {
        // Shift+Enter in list: Create new list item
        e.preventDefault()
        const newLi = document.createElement('li')
        newLi.innerHTML = '<br>'
        listItem.parentNode.insertBefore(newLi, listItem.nextSibling)
        
        // Move cursor to new list item
        const range = document.createRange()
        const sel = window.getSelection()
        range.setStart(newLi, 0)
        range.collapse(true)
        sel.removeAllRanges()
        sel.addRange(range)
        
        // Update content
        setContent(editorRef.current.innerHTML)
        return
      } else if (e.shiftKey) {
        // Shift+Enter not in list: new line (browser default)
        return
      } else {
        // Enter without Shift: Always send message
        e.preventDefault()
        send()
        return
      }
    }

    // Formatting shortcuts
    if (e.ctrlKey || e.metaKey) {
      switch (e.key.toLowerCase()) {
        case 'b':
          e.preventDefault()
          applyFormat('bold')
          break
        case 'i':
          e.preventDefault()
          applyFormat('italic')
          break
        case 'u':
          e.preventDefault()
          applyFormat('underline')
          break
        case 'k':
          e.preventDefault()
          applyFormat('link')
          break
        default:
          break
      }
    }
  }

  const handleInput = () => {
    const editor = editorRef.current
    if (editor) {
      setContent(editor.innerHTML)
    }
  }

  const placeholder = isDM ? `Message ${channelName || 'user'}` : `Message #${channelName || 'channel'}`
  const isEmpty = !content || content === '<br>' || content === '<ol><li><br></li></ol>' || content === '<ul><li><br></li></ul>' || editorRef.current?.innerText.trim() === ''

  return (
    <div className="composer">
      <div className="composer-inner">
        <div className="composer-container">
                {/* Formatting toolbar */}
                {showFormatting && (
                  <div className="composer-toolbar">
                        <button className="toolbar-btn" onClick={() => applyFormat('bold')} title="Bold">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M4 2.75A.75.75 0 0 1 4.75 2h6.343a3.91 3.91 0 0 1 3.88 3.449A2 2 0 0 1 15 5.84l.001.067a3.9 3.9 0 0 1-1.551 3.118A4.627 4.627 0 0 1 11.875 18H4.75a.75.75 0 0 1-.75-.75V9.5a.8.8 0 0 1 .032-.218A.8.8 0 0 1 4 9.065zm2.5 5.565h3.593a2.157 2.157 0 1 0 0-4.315H6.5zm4.25 1.935H6.5v5.5h4.25a2.75 2.75 0 1 0 0-5.5" clipRule="evenodd"></path></svg>
                        </button>
                        <button className="toolbar-btn" onClick={() => applyFormat('italic')} title="Italic">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M7 2.75A.75.75 0 0 1 7.75 2h7.5a.75.75 0 0 1 0 1.5H12.3l-2.6 13h2.55a.75.75 0 0 1 0 1.5h-7.5a.75.75 0 0 1 0-1.5H7.7l2.6-13H7.75A.75.75 0 0 1 7 2.75" clipRule="evenodd"></path></svg>
                        </button>
                        <button className="toolbar-btn" onClick={() => applyFormat('underline')} title="Underline">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" d="M17.25 17.12a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5zM14.5 1.63a.75.75 0 0 1 .75.75v8a5.25 5.25 0 1 1-10.5 0v-8a.75.75 0 0 1 1.5 0v8a3.75 3.75 0 0 0 7.5 0v-8a.75.75 0 0 1 .75-.75"></path></svg>
                        </button>
                        <button className="toolbar-btn" onClick={() => applyFormat('strikethrough')} title="Strikethrough">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M11.721 3.84c-.91-.334-2.028-.36-3.035-.114-1.51.407-2.379 1.861-2.164 3.15C6.718 8.051 7.939 9.5 11.5 9.5l.027.001h5.723a.75.75 0 0 1 0 1.5H2.75a.75.75 0 0 1 0-1.5h3.66c-.76-.649-1.216-1.468-1.368-2.377-.347-2.084 1.033-4.253 3.265-4.848l.007-.002.007-.002c1.252-.307 2.68-.292 3.915.16 1.252.457 2.337 1.381 2.738 2.874a.75.75 0 0 1-1.448.39c-.25-.925-.91-1.528-1.805-1.856m2.968 9.114a.75.75 0 1 0-1.378.59c.273.64.186 1.205-.13 1.674-.333.492-.958.925-1.82 1.137-.989.243-1.991.165-3.029-.124-.93-.26-1.613-.935-1.858-1.845a.75.75 0 0 0-1.448.39c.388 1.441 1.483 2.503 2.903 2.9 1.213.338 2.486.456 3.79.135 1.14-.28 2.12-.889 2.704-1.753.6-.888.743-1.992.266-3.104" clipRule="evenodd"></path></svg>
                        </button>
                        <span className="toolbar-separator"></span>
                        <button className="toolbar-btn" onClick={() => applyFormat('link')} title="Link">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M12.306 3.756a2.75 2.75 0 0 1 3.889 0l.05.05a2.75 2.75 0 0 1 0 3.889l-3.18 3.18a2.75 2.75 0 0 1-3.98-.095l-.03-.034a.75.75 0 0 0-1.11 1.009l.03.034a4.25 4.25 0 0 0 6.15.146l3.18-3.18a4.25 4.25 0 0 0 0-6.01l-.05-.05a4.25 4.25 0 0 0-6.01 0L9.47 4.47a.75.75 0 1 0 1.06 1.06zm-4.611 12.49a2.75 2.75 0 0 1-3.89 0l-.05-.051a2.75 2.75 0 0 1 0-3.89l3.18-3.179a2.75 2.75 0 0 1 3.98.095l.03.034a.75.75 0 1 0 1.11-1.01l-.03-.033a4.25 4.25 0 0 0-6.15-.146l-3.18 3.18a4.25 4.25 0 0 0 0 6.01l.05.05a4.25 4.25 0 0 0 6.01 0l1.775-1.775a.75.75 0 0 0-1.06-1.06z" clipRule="evenodd"></path></svg>
                        </button>
                        <button className="toolbar-btn" onClick={() => applyFormat('orderedList')} title="Numbered list">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M3.792 2.094A.5.5 0 0 1 4 2.5V6h1a.5.5 0 1 1 0 1H2a.5.5 0 1 1 0-1h1V3.194l-.842.28a.5.5 0 0 1-.316-.948l1.5-.5a.5.5 0 0 1 .45.068M7.75 3.5a.75.75 0 0 0 0 1.5h10a.75.75 0 0 0 0-1.5zM7 10.75a.75.75 0 0 1 .75-.75h10a.75.75 0 0 1 0 1.5h-10a.75.75 0 0 1-.75-.75m0 6.5a.75.75 0 0 1 .75-.75h10a.75.75 0 0 1 0 1.5h-10a.75.75 0 0 1-.75-.75m-4.293-3.36a1 1 0 0 1 .793-.39c.49 0 .75.38.75.75 0 .064-.033.194-.173.409a5 5 0 0 1-.594.711c-.256.267-.552.548-.87.848l-.088.084a42 42 0 0 0-.879.845A.5.5 0 0 0 2 18h3a.5.5 0 0 0 0-1H3.242l.058-.055c.316-.298.629-.595.904-.882a6 6 0 0 0 .711-.859c.18-.277.335-.604.335-.954 0-.787-.582-1.75-1.75-1.75a2 2 0 0 0-1.81 1.147.5.5 0 1 0 .905.427 1 1 0 0 1 .112-.184" clipRule="evenodd"></path></svg>
                        </button>
                        <button className="toolbar-btn" onClick={() => applyFormat('unorderedList')} title="Bullet list">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M4 3a1 1 0 1 1-2 0 1 1 0 0 1 2 0m3 0a.75.75 0 0 1 .75-.75h10a.75.75 0 0 1 0 1.5h-10A.75.75 0 0 1 7 3m.75 6.25a.75.75 0 0 0 0 1.5h10a.75.75 0 0 0 0-1.5zm0 7a.75.75 0 0 0 0 1.5h10a.75.75 0 0 0 0-1.5zM3 11a1 1 0 1 0 0-2 1 1 0 0 0 0 2m0 7a1 1 0 1 0 0-2 1 1 0 0 0 0 2" clipRule="evenodd"></path></svg>
                        </button>
                        <span className="toolbar-separator"></span>
                        <button className="toolbar-btn" onClick={() => applyFormat('blockquote')} title="Block quote">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M3.5 2.75a.75.75 0 0 0-1.5 0v14.5a.75.75 0 0 0 1.5 0zM6.75 3a.75.75 0 0 0 0 1.5h8.5a.75.75 0 0 0 0-1.5zM6 10.25a.75.75 0 0 1 .75-.75h10.5a.75.75 0 0 1 0 1.5H6.75a.75.75 0 0 1-.75-.75m.75 5.25a.75.75 0 0 0 0 1.5h7.5a.75.75 0 0 0 0-1.5z" clipRule="evenodd"></path></svg>
                        </button>
                        <button className="toolbar-btn" onClick={() => applyFormat('code')} title="Code">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M12.058 3.212c.396.12.62.54.5.936L8.87 16.29a.75.75 0 1 1-1.435-.436l3.686-12.143a.75.75 0 0 1 .936-.5M5.472 6.24a.75.75 0 0 1 .005 1.06l-2.67 2.693 2.67 2.691a.75.75 0 1 1-1.065 1.057l-3.194-3.22a.75.75 0 0 1 0-1.056l3.194-3.22a.75.75 0 0 1 1.06-.005m9.044 1.06a.75.75 0 1 1 1.065-1.056l3.194 3.221a.75.75 0 0 1 0 1.057l-3.194 3.219a.75.75 0 0 1-1.065-1.057l2.67-2.69z" clipRule="evenodd"></path></svg>
                        </button>
                        <button className="toolbar-btn" onClick={() => applyFormat('codeBlock')} title="Code block">
                          <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M9.212 2.737a.75.75 0 1 0-1.424-.474l-2.5 7.5a.75.75 0 0 0 1.424.474zm6.038.265a.75.75 0 0 0 0 1.5h2a.25.25 0 0 1 .25.25v11.5a.25.25 0 0 1-.25.25h-13a.25.25 0 0 1-.25-.25v-3.5a.75.75 0 0 0-1.5 0v3.5c0 .966.784 1.75 1.75 1.75h13a1.75 1.75 0 0 0 1.75-1.75v-11.5a1.75 1.75 0 0 0-1.75-1.75zm-3.69.5a.75.75 0 1 0-1.12.996l1.556 1.754-1.556 1.75a.75.75 0 1 0 1.12.997l2-2.249a.75.75 0 0 0 0-.996zM3.999 9.061a.75.75 0 0 1-1.058-.062l-2-2.249a.75.75 0 0 1 0-.996l2-2.252a.75.75 0 1 1 1.12.996L2.504 6.252l1.557 1.75a.75.75 0 0 1-.062 1.059" clipRule="evenodd"></path></svg>
                        </button>
                  </div>
                )}

                {/* Editor */}
                <div className="editor-container">
                  <div 
                    ref={editorRef}
                    className="editor-unstyled"
                    contentEditable="true"
                    onInput={handleInput}
                    onKeyDown={handleKeyDown}
                    role="textbox"
                    aria-label={placeholder}
                    data-placeholder={placeholder}
                    suppressContentEditableWarning={true}
                  />
                </div>

                {/* File attachments preview */}
                {selectedFiles.length > 0 && (
                  <div className="file-attachments-preview">
                    {selectedFiles.map((file, index) => (
                      <div key={index} className="file-attachment-item">
                        <span className="file-name">{file.name}</span>
                        <button onClick={() => removeFile(index)} className="file-remove">×</button>
                      </div>
                    ))}
                  </div>
                )}

                {/* Footer toolbar */}
                <div className="composer-footer">
                  <div className="composer-prefix">
                    <button className="composer-button" onClick={() => fileInputRef.current?.click()} title="Attach">
                      <svg viewBox="0 0 20 20"><path fill="currentColor" fillRule="evenodd" d="M10.75 3.25a.75.75 0 0 0-1.5 0v6H3.251L3.25 10v-.75a.75.75 0 0 0 0 1.5V10v.75h6v6a.75.75 0 0 0 1.5 0v-6h6a.75.75 0 0 0 0-1.5h-6z" clipRule="evenodd"></path></svg>
                    </button>
                    <input 
                      ref={fileInputRef}
                      type="file" 
                      multiple 
                      onChange={handleFileSelect}
                      style={{ display: 'none' }}
                    />
                  </div>

                  <div className="composer-toolbar_buttons">
                    <button className="composer-button" onClick={() => setShowFormatting(!showFormatting)} title="Show formatting" aria-pressed={showFormatting}>
                      <svg viewBox="0 0 20 20" style={{ width: '18px' }}><path fill="currentColor" fillRule="evenodd" d="M6.941 3.952c-.459-1.378-2.414-1.363-2.853.022l-4.053 12.8a.75.75 0 0 0 1.43.452l1.101-3.476h6.06l1.163 3.487a.75.75 0 1 0 1.423-.474zm1.185 8.298L5.518 4.427 3.041 12.25zm6.198-5.537a4.74 4.74 0 0 1 3.037-.081A3.74 3.74 0 0 1 20 10.208V17a.75.75 0 0 1-1.5 0v-.745a8 8 0 0 1-2.847 1.355 3 3 0 0 1-3.15-1.143C10.848 14.192 12.473 11 15.287 11H18.5v-.792c0-.984-.641-1.853-1.581-2.143a3.24 3.24 0 0 0-2.077.056l-.242.089a2.22 2.22 0 0 0-1.34 1.382l-.048.145a.75.75 0 0 1-1.423-.474l.048-.145a3.72 3.72 0 0 1 2.244-2.315zM18.5 12.5h-3.213c-1.587 0-2.504 1.801-1.57 3.085.357.491.98.717 1.572.57a6.5 6.5 0 0 0 2.47-1.223l.741-.593z" clipRule="evenodd"></path></svg>
                    </button>
                    <div className="emoji-picker-wrapper">
                      <button className="composer-button" onClick={() => setShowEmojiPicker(!showEmojiPicker)} title="Emoji">
                        <svg viewBox="0 0 20 20" style={{ width: '18px' }}><path fill="currentColor" fillRule="evenodd" d="M2.5 10a7.5 7.5 0 1 1 15 0 7.5 7.5 0 0 1-15 0M10 1a9 9 0 1 0 0 18 9 9 0 0 0 0-18M7.5 9.5a1.5 1.5 0 1 0 0-3 1.5 1.5 0 0 0 0 3M14 8a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0m-6.385 3.766a.75.75 0 1 0-1.425.468C6.796 14.08 8.428 15 10.027 15s3.23-.92 3.838-2.766a.75.75 0 1 0-1.425-.468c-.38 1.155-1.38 1.734-2.413 1.734s-2.032-.58-2.412-1.734" clipRule="evenodd"></path></svg>
                      </button>
                      {showEmojiPicker && (
                        <div className="emoji-picker-popup">
                          {commonEmojis.map((emoji, i) => (
                            <button key={i} className="emoji-item" onClick={() => insertEmoji(emoji)}>
                              {emoji}
                            </button>
                          ))}
                        </div>
                      )}
                    </div>
                    <button className="composer-button" onClick={showMentionPickerAtCursor} title="Mention someone">
                      <svg viewBox="0 0 20 20" style={{ width: '18px' }}><path fill="currentColor" fillRule="evenodd" d="M2.5 10a7.5 7.5 0 1 1 15 0v.645c0 1.024-.83 1.855-1.855 1.855a1.145 1.145 0 0 1-1.145-1.145V6.75a.75.75 0 0 0-1.494-.098 4.5 4.5 0 1 0 .465 6.212A2.64 2.64 0 0 0 15.646 14 3.355 3.355 0 0 0 19 10.645V10a9 9 0 1 0-3.815 7.357.75.75 0 1 0-.865-1.225A7.5 7.5 0 0 1 2.5 10m7.5 3a3 3 0 1 0 0-6 3 3 0 0 0 0 6" clipRule="evenodd"></path></svg>
                    </button>
                  </div>

                  <div className="composer-suffix">
                    <span className="composer-send_button">
                      <button 
                        className={`composer-button composer-button--send ${isEmpty ? 'composer-button--disabled' : ''}`}
                        onClick={send}
                        disabled={isEmpty && selectedFiles.length === 0}
                        title="Send now"
                      >
                        <svg viewBox="0 0 20 20"><path fill="currentColor" d="M1.5 2.106c0-.462.498-.754.901-.528l15.7 7.714a.73.73 0 0 1 .006 1.307L2.501 18.46l-.07.017a.754.754 0 0 1-.931-.733v-4.572c0-1.22.971-2.246 2.213-2.268l6.547-.17c.27-.01.75-.243.75-.797 0-.553-.5-.795-.75-.795l-6.547-.171C2.47 8.95 1.5 7.924 1.5 6.704z"></path></svg>
                      </button>
                    </span>
                  </div>
                </div>
        </div>
      </div>

      {/* Mention picker popup - positioned absolutely */}
      {showMentionPicker && (
        <div 
          className="mention-picker-popup" 
          ref={mentionPickerRef}
          style={{
            top: `${mentionPickerPosition.top}px`,
            left: `${mentionPickerPosition.left}px`
          }}
        >
          <div className="mention-picker-header">
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" style={{ opacity: 0.7 }}>
                <path d="M6 2L6 10M3 7L6 10L9 7" stroke="#d1d2d3" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                <path d="M6 10L6 2M3 5L6 2L9 5" stroke="#d1d2d3" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span style={{ fontSize: '11px', fontWeight: '600', color: '#d1d2d3' }}>to navigate</span>
            </div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '4px', marginLeft: '12px' }}>
              <svg width="12" height="12" viewBox="0 0 12 12" fill="none" style={{ opacity: 0.7 }}>
                <rect x="2" y="2" width="8" height="8" rx="2" stroke="#9a9a9a" strokeWidth="1.5"/>
                <path d="M4 6L5.5 7.5L8 4.5" stroke="#9a9a9a" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              <span style={{ fontSize: '11px', color: '#9a9a9a' }}>to select</span>
            </div>
          </div>
          <div className="mention-picker-contacts">
            {contacts.map((contact) => (
              <div 
                key={contact.id} 
                className="mention-contact-item"
                onClick={() => insertMention(contact)}
              >
                {contact.profile_picture ? (
                  <img 
                    src={contact.profile_picture} 
                    alt={contact.name}
                    className="mention-contact-avatar-img"
                  />
                ) : (
                  <div className="mention-contact-avatar">
                    {contact.name?.charAt(0) || '?'}
                  </div>
                )}
                <div className="mention-contact-info">
                  <div className="mention-contact-name">{contact.name}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
