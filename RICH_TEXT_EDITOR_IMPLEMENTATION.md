# Rich Text Editor Implementation Guide

## Overview
This guide details the implementation of a Slack-style rich text editor with full formatting capabilities, file attachments, and persistent storage.

## Features Implemented

### 1. Text Formatting
- **Bold** (Ctrl+B)
- *Italic* (Ctrl+I)
- <u>Underline</u> (Ctrl+U)
- ~~Strikethrough~~ (Ctrl+Shift+X)

### 2. Lists
- Numbered lists (Ctrl+Shift+7)
- Bullet lists (Ctrl+Shift+8)

### 3. Code & Quotes
- `Inline code` (Ctrl+Shift+C)
- ```Code blocks``` (Ctrl+Shift+K)
- Block quotes (Ctrl+Shift+9)

### 4. Links & Media
- Hyperlinks (Ctrl+K)
- File attachments (drag & drop or click)
- Emoji picker
- @mentions

### 5. Additional Features
- Video clips
- Audio clips
- Shortcuts menu
- Send scheduling

## Technology Stack

### Frontend
- **React** with hooks
- **react-quill** or **slate.js** for rich text editing
- **emoji-picker-react** for emoji selection
- **react-dropzone** for file uploads

### Backend Storage
- Messages stored with HTML/Markdown format
- File metadata and URLs stored separately
- Formatting preserved in database

## Database Schema Updates

```sql
-- Add formatting column to messages
ALTER TABLE messages ADD COLUMN formatted_content TEXT;
ALTER TABLE messages ADD COLUMN content_format VARCHAR(20) DEFAULT 'html'; -- 'html', 'markdown', or 'plain'

-- Add attachments table
CREATE TABLE IF NOT EXISTS message_attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    message_id INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(100),
    file_size INTEGER,
    file_url TEXT NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (message_id) REFERENCES messages(id)
);

-- Same for DMs
ALTER TABLE direct_messages ADD COLUMN formatted_content TEXT;
ALTER TABLE direct_messages ADD COLUMN content_format VARCHAR(20) DEFAULT 'html';

CREATE TABLE IF NOT EXISTS dm_attachments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    direct_message_id INTEGER NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(100),
    file_size INTEGER,
    file_url TEXT NOT NULL,
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (direct_message_id) REFERENCES direct_messages(id)
);
```

## Implementation Steps

### Step 1: Install Dependencies
```bash
npm install react-quill quill emoji-picker-react react-dropzone
```

### Step 2: Create RichTextComposer Component
Located at: `frontend/src/components/RichTextComposer.jsx`

### Step 3: Update Backend API
- Modify message POST endpoints to accept formatted_content
- Add file upload endpoint
- Store formatting metadata

### Step 4: Message Display
- Render HTML/Markdown content safely
- Display attachments with icons
- Show formatting in message history

### Step 5: Keyboard Shortcuts
Implement all formatting shortcuts for better UX

## Quick Start

### Run Database Migration
```bash
cd "c:\Users\Abcom\Desktop\ScalerAI hackathon\slack-rl-clone"
python migrate_rich_text.py
```

### Install Frontend Dependencies
```bash
cd frontend
npm install react-quill quill emoji-picker-react react-dropzone
```

### Update Message Components
Replace MessageInput with RichTextComposer in:
- ChannelPage.jsx
- DMPage.jsx

## SVG Icons Reference

All formatting icons are available in the HTML code provided:
- Bold, Italic, Underline, Strikethrough
- Link, Lists (numbered/bulleted)
- Code, Code Block, Block Quote
- Plus (attach), Emoji, Mentions
- Video, Audio, Shortcuts
- Send button

## Security Considerations

1. **XSS Prevention**: Sanitize HTML content before rendering
2. **File Upload**: Validate file types and sizes
3. **Storage Limits**: Implement file size and storage quotas

## Browser Compatibility

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Performance Optimization

1. Lazy load emoji picker
2. Compress uploaded files
3. Use virtual scrolling for long message history
4. Debounce auto-save

## Testing Checklist

- [ ] All formatting buttons work
- [ ] Keyboard shortcuts functional
- [ ] File upload and preview
- [ ] Emoji insertion
- [ ] @mentions autocomplete
- [ ] Link creation and editing
- [ ] Message persistence
- [ ] Cross-browser testing
- [ ] Mobile responsiveness

## Future Enhancements

1. Collaborative editing
2. Message reactions
3. Thread replies
4. Message search with formatting
5. Export conversations
6. Voice messages
7. Screen sharing
8. Custom emojis
9. Message templates
10. Integration with external tools

## Support

For issues or questions, refer to:
- React Quill docs: https://github.com/zenoamaro/react-quill
- Slate.js docs: https://docs.slatejs.org/
- Emoji Picker: https://github.com/ealush/emoji-picker-react
