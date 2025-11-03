# Frontend Setup Guide - React + Vite

## Prerequisites
- Node.js (v16 or higher recommended)
- npm (comes with Node.js)

## Setup Steps

### 1. Navigate to the frontend folder
```powershell
cd "c:\Users\Abcom\Desktop\ScalerAI hackathon\slack-rl-clone\frontend"
```

### 2. Install dependencies
```powershell
npm install
```

This will install:
- React & React DOM
- React Router (for navigation)
- Axios (for API calls)
- Vite (build tool)
- Tailwind CSS (styling)
- Lucide React (icons)
- @vitejs/plugin-react (Vite React plugin)

### 3. Start the development server
```powershell
npm run dev
```

The app should start on **http://localhost:5173**

### 4. Expected Output
You should see:
```
  VITE v5.2.0  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### 5. Open in Browser
Navigate to: **http://localhost:5173**

## Troubleshooting

### If you get "cannot find module" errors:
```powershell
rm -r node_modules
rm package-lock.json
npm install
```

### If port 5173 is already in use:
```powershell
npm run dev -- --port 5174
```

### If Vite config errors occur:
Make sure `vite.config.js` exists with:
```js
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
})
```

## Project Structure
```
frontend/
├── src/
│   ├── api/
│   │   └── axios.js          # API configuration
│   ├── components/
│   │   ├── Sidebar.jsx       # Channel sidebar
│   │   ├── ChatWindow.jsx    # Messages display
│   │   └── MessageInput.jsx  # Send messages
│   ├── pages/
│   │   ├── ChannelPage.jsx   # Channel view
│   │   └── DMPage.jsx         # DM view (placeholder)
│   ├── styles/
│   │   ├── global.css        # Global styles + CSS variables
│   │   ├── App.css           # App layout
│   │   ├── Sidebar.css       # Sidebar styles
│   │   ├── ChatWindow.css    # Chat styles
│   │   └── MessageInput.css  # Input styles
│   ├── App.jsx               # Main app component
│   ├── main.jsx              # Entry point
│   └── index.css             # (legacy, uses global.css now)
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.cjs
├── postcss.config.cjs
└── .env                       # API URL config

```

## Important Notes

1. **Backend must be running** on http://localhost:8000 for the frontend to work
2. The `.env` file sets the API URL: `VITE_API_URL=http://localhost:8000`
3. Default user ID is hardcoded as `1` in MessageInput component
4. Hot reload is enabled - changes auto-refresh in browser

## Next Steps After Starting

1. Make sure backend is running (see backend setup)
2. Navigate to http://localhost:5173
3. Click on a channel in the sidebar (e.g., "general")
4. Type and send messages
5. Toggle dark/light theme using the button in top bar

## Common Commands

```powershell
# Start dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Install a new package
npm install <package-name>
```
