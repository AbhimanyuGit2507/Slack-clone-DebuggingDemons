# Slack Clone - ScalerAI Hackathon 2025

**Team: DebuggingDemons**

A high-fidelity, full-stack Slack clone built with React and FastAPI, featuring real-time messaging, channels, direct messages, canvas collaboration.

---

## Judge quick start (recommended)

These steps will build and run both the frontend and backend containers using Docker Compose. The included `docker-compose.yml` is configured so the frontend (nginx) proxies `/api/*` to the backend service automatically — no extra configuration is required for a local judge run.

From repository root:

```powershell
# 1. Clone the repository
git clone https://github.com/AbhimanyuGit2507/Slack-clone-DebuggingDemons.git

# 2. Enter the project directory
cd Slack-clone-DebuggingDemons

# 3. Build and start the app
docker compose up --build -d

# 4. Tail logs (optional)
docker compose logs -f --tail=200 backend frontend
```

Open the frontend in a browser: http://localhost:3000

Notes:
- Frontend (nginx) is served on host port 3000 and proxies `/api` to the backend container internally.
- Backend API is available on host port 8000 (http://localhost:8000/docs for FastAPI docs).
- Database and uploads persist to `./data` and `./uploads` on the host (see `docker-compose.yml`).

The backend startup script will seed the database the first time the container runs. If you'd like to reset data, stop the compose stack and remove `./data` then restart.

---

## 📋 Project Overview

This project is a **high-fidelity fullstack clone of Slack**, built as part of the ScalerAI Hackathon. The goal is to deliver a highly interactive, visually smooth, and logically consistent user experience that demonstrates the ability to design and implement a complete web application combining strong frontend design and user interaction handling with robust backend logic for data management and synchronization



## 🎯 Assignment Objectives


This assignment evaluates the following capabilities:## 🚀 FeaturesOverview

- **Frontend Design**: Creating a visually polished, responsive UI that closely mimics Slack's design language

- **User Interaction**: Implementing smooth, intuitive user interactions with proper state management- Frontend: React + Vite + Tailwind

- **Backend Architecture**: Building a scalable REST API with proper data models and relationships

- **Fullstack Integration**: Seamless communication between frontend and backend### Core Features- Backend: FastAPI + SQLite (SQLAlchemy)

- **Data Management**: Efficient data storage, retrieval, and synchronization

- **Code Quality**: Clean, maintainable, and well-documented code- **Real-time Messaging**: Send and receive messages in channels and direct messages



## 🚀 Features- **Channels**: Create and manage public/private channels with descriptionsRun (two terminals)



### Core Messaging Features- **Direct Messages**: One-on-one conversations with other users- Frontend: cd frontend; npm install; npm run dev

- ✅ **Real-time Messaging**: Send and receive messages in channels and direct messages

- ✅ **Channels**: Create and manage public/private channels with descriptions- **Canvas Collaboration**: Collaborative canvas for team brainstorming and notes- Backend: python -m venv .venv (optional); .venv\Scripts\activate; pip install -r requirements.txt; uvicorn backend.main:app --reload

- ✅ **Direct Messages**: One-on-one conversations with other users

- ✅ **Rich Text Editor**: Format messages with bold, italic, lists, code blocks, and links- **File Sharing**: Upload and share files within channels and DMs

- ✅ **Message Editing & Deletion**: Edit or delete your own messages

- ✅ **Emoji Support**: Add emojis to messages and reactions- **Activity Feed**: Track mentions, reactions, and important updatesStructure



### Collaboration Features- **Starred Items**: Star important channels, DMs, messages, and files```

- ✅ **Canvas Collaboration**: Collaborative canvas for team brainstorming and notes with auto-save

- ✅ **File Sharing**: Upload and share files within channels and DMs- **Search**: Search messages, files, and conversationsslack-rl-clone/

- ✅ **Activity Feed**: Track mentions, reactions, and important updates

- ✅ **Starred Items**: Star important channels, DMs, messages, and files for quick access- **User Directories**: Browse and connect with team members├── frontend/

- ✅ **Search**: Search messages, files, and conversations

- ✅ **User Directories**: Browse and connect with team members├── backend/



### UI/UX Features### UI Features├── data/

- ✅ **Responsive Design**: Optimized for desktop and mobile devices

- ✅ **Dark Mode Ready**: Professional dark theme interface- **Responsive Design**: Works seamlessly on desktop and mobile├── README.md

- ✅ **Smooth Animations**: Framer Motion powered transitions

- ✅ **Drag & Drop**: File uploads with drag-and-drop support- **Dark Mode Ready**: Clean, professional interface└── requirements.txt

- ✅ **Resizable Panels**: Adjustable sidebar widths

- ✅ **Profile Customization**: Set profile pictures and status messages- **Rich Text Editor**: Format messages with bold, italic, lists, and more```

- ✅ **Recently Viewed**: Track recently accessed canvases and conversations

- **Emoji Support**: Add emojis to messages and reactions

## 🛠️ Tech Stack

- **File Attachments**: Drag-and-drop file uploadsNotes

### Frontend

- **React 18**: Modern React with hooks and functional components- **Profile Customization**: Set profile pictures and status- this is a simulation for RL experiments.

- **React Router v6**: Client-side routing and navigation

- **Framer Motion**: Smooth animations and transitions- API base: http://localhost:8000 (set via frontend/.env)

- **Axios**: HTTP client for API requests

- **Lucide React**: Modern, customizable icon library## 🛠️ Tech Stack

- **Vite**: Lightning-fast build tool and dev server

- **CSS3**: Custom styling with modern CSS features### Frontend

- **React 18**: Modern React with hooks

### Backend- **React Router**: Client-side routing

- **FastAPI**: Modern, high-performance Python web framework- **Framer Motion**: Smooth animations and transitions

- **SQLAlchemy**: Powerful SQL toolkit and ORM- **Axios**: HTTP client for API requests

- **SQLite**: Lightweight database (production-ready for PostgreSQL/MySQL)- **Lucide React**: Modern icon library

- **Pydantic**: Data validation using Python type hints- **Vite**: Fast build tool and dev server

- **Uvicorn**: Lightning-fast ASGI server

- **Python 3.11+**: Latest Python features### Backend

- **FastAPI**: Modern Python web framework

### DevOps- **SQLAlchemy**: SQL toolkit and ORM

- **Docker**: Containerization for easy deployment- **SQLite**: Database (easily switchable to PostgreSQL/MySQL)

- **Docker Compose**: Multi-container orchestration- **Pydantic**: Data validation using Python type hints

- **Git**: Version control- **Uvicorn**: ASGI server



## 📋 Prerequisites## 📋 Prerequisites



### Option 1: Docker (Recommended)- **Docker** and **Docker Compose** installed on your system

- Docker Desktop (Windows/Mac) or Docker Engine (Linux)- **Git** for cloning the repository

- Docker Compose v2.0+

- GitOR



### Option 2: Manual Setup- **Node.js 18+** and **npm**

- Node.js 18+ and npm- **Python 3.11+** and **pip**

- Python 3.11+

- Git## 🐳 Quick Start with Docker (Recommended)



## 🐳 Quick Start with Docker (Recommended)### 1. Clone the repository



### 1. Clone the repository```bash

git clone https://github.com/yourusername/slack-rl-clone.git

```bashcd slack-rl-clone

git clone https://github.com/yourusername/slack-rl-clone.git```

cd slack-rl-clone

```### 2. Start the application



### 2. Start the application```bash

docker-compose up --build

```bash```

docker-compose up --build

```This will:

- Build both frontend and backend Docker images

This command will:- Start the backend API server on `http://localhost:8000`

- Build Docker images for both frontend and backend- Start the frontend dev server on `http://localhost:5173`

- Initialize SQLite database with sample data- Create and initialize the SQLite database with sample data

- Start backend API server on `http://localhost:8000`

- Start frontend dev server on `http://localhost:5173`### 3. Access the application



### 3. Access the applicationOpen your browser and navigate to:

- **Frontend**: http://localhost:5173

Open your browser and navigate to:- **Backend API Docs**: http://localhost:8000/docs

- **Frontend Application**: http://localhost:5173

- **Backend API Documentation**: http://localhost:8000/docs### 4. Stop the application

- **Alternative API Docs**: http://localhost:8000/redoc

```bash

### 4. Stop the applicationdocker-compose down

```

Press `Ctrl+C` in the terminal, then run:

## 💻 Manual Setup (Without Docker)

```bash

docker-compose down### Backend Setup

```

1. Navigate to the backend directory:

To remove all data and start fresh:```bash

cd backend

```bash```

docker-compose down -v

```2. Create a virtual environment:

```bash

## 💻 Manual Setup (Without Docker)python -m venv venv

source venv/bin/activate  # On Windows: venv\Scripts\activate

### Backend Setup```



1. **Navigate to backend directory:**3. Install dependencies:

   ```bash```bash

   cd backendpip install -r requirements.txt

   ``````



2. **Create and activate virtual environment:**4. Initialize the database:

   ```bash```bash

   # Windowspython seed.py

   python -m venv venv```

   venv\Scripts\activate

5. Start the backend server:

   # Mac/Linux```bash

   python3 -m venv venvuvicorn main:app --reload

   source venv/bin/activate```

   ```

The API will be available at `http://localhost:8000`

3. **Install dependencies:**

   ```bash### Frontend Setup

   pip install -r requirements.txt

   ```1. Navigate to the frontend directory:

```bash

4. **Initialize database with sample data:**cd frontend

   ```bash```

   python seed.py

   ```2. Install dependencies:

```bash

5. **Start the backend server:**npm install

   ```bash```

   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   ```3. Start the development server:

```bash

### Frontend Setupnpm run dev

```

1. **Navigate to frontend directory (in a new terminal):**

   ```bashThe application will be available at `http://localhost:5173`

   cd frontend

   ```## 📁 Project Structure



2. **Install dependencies:**```

   ```bashslack-rl-clone/

   npm install├── backend/

   ```│   ├── main.py              # FastAPI application entry point

│   ├── database.py          # Database configuration

3. **Start the development server:**│   ├── models.py            # SQLAlchemy models

   ```bash│   ├── schemas.py           # Pydantic schemas

   npm run dev│   ├── seed.py              # Database seeding script

   ```│   ├── requirements.txt     # Python dependencies

│   ├── Dockerfile           # Backend Docker configuration

## 📁 Project Structure│   └── routes/

│       ├── auth.py          # Authentication endpoints

```│       ├── channels.py      # Channel management

slack-rl-clone/│       ├── messages.py      # Message handling

├── backend/│       ├── direct_messages.py  # DM functionality

│   ├── main.py                 # FastAPI application entry point│       ├── canvas.py        # Canvas collaboration

│   ├── database.py             # Database configuration and session│       └── attachments.py   # File handling

│   ├── models.py               # SQLAlchemy ORM models├── frontend/

│   ├── schemas.py              # Pydantic schemas for validation│   ├── src/

│   ├── seed.py                 # Database seeding with sample data│   │   ├── components/      # React components

│   ├── requirements.txt        # Python dependencies│   │   ├── pages/           # Page components

│   ├── Dockerfile              # Backend Docker configuration│   │   ├── styles/          # CSS styles

│   ├── uploads/                # File upload storage│   │   ├── hooks/           # Custom React hooks

│   └── routes/│   │   ├── api/             # API client configuration

│       ├── auth.py             # User authentication (disabled for demo)│   │   └── assets/          # Static assets

│       ├── users.py            # User management endpoints│   ├── package.json         # Node dependencies

│       ├── channels.py         # Channel CRUD operations│   ├── vite.config.js       # Vite configuration

│       ├── messages.py         # Message handling│   └── Dockerfile           # Frontend Docker configuration

│       ├── direct_messages.py  # Direct messaging├── docker-compose.yml       # Docker Compose configuration

│       ├── canvas.py           # Canvas collaboration└── README.md               # This file

│       └── attachments.py      # File upload/download```

├── frontend/

│   ├── src/## 🗄️ Database Schema

│   │   ├── components/         # Reusable React components

│   │   │   ├── TopNav.jsx      # Top navigation bar### Core Tables

│   │   │   ├── IconNav.jsx     # Left icon navigation- **users**: User accounts and profiles

│   │   │   ├── Sidebar.jsx     # Channel/DM sidebar- **channels**: Channel information

│   │   │   ├── Canvas.jsx      # Collaborative canvas- **channel_members**: Channel membership

│   │   │   └── ...- **messages**: Channel messages

│   │   ├── pages/              # Page-level components- **direct_messages**: Direct message conversations

│   │   │   ├── HomePage.jsx- **canvas**: Collaborative canvas documents

│   │   │   ├── ChannelPage.jsx- **attachments**: File uploads and metadata

│   │   │   ├── DMPage.jsx

│   │   │   ├── FilesPage.jsx## 🔧 Configuration

│   │   │   └── ...

│   │   ├── styles/             # CSS stylesheets### Environment Variables

│   │   ├── hooks/              # Custom React hooks

│   │   │   └── usePageTitle.js # Dynamic page titles**Backend** (`.env` in backend directory):

│   │   ├── api/                # API client```env

│   │   │   └── axios.js        # Axios configurationDATABASE_URL=sqlite:///./slack.db

│   │   ├── assets/             # Static assets (images, icons)SECRET_KEY=your-secret-key-here

│   │   └── App.jsx             # Main application component```

│   ├── package.json            # Node dependencies

│   ├── vite.config.js          # Vite configuration**Frontend** (`.env` in frontend directory):

│   ├── Dockerfile              # Frontend Docker configuration```env

│   └── index.html              # HTML entry pointVITE_API_URL=http://localhost:8000

├── docker-compose.yml          # Docker Compose orchestration```

├── .gitignore                  # Git ignore patterns

├── README.md                   # This file## 📝 API Documentation

├── SETUP.md                    # Detailed setup instructions

└── API.md                      # Complete API documentationOnce the backend is running, access the interactive API documentation:

```- **Swagger UI**: http://localhost:8000/docs

- **ReDoc**: http://localhost:8000/redoc

## 🗄️ Database Schema

## 🎯 Key Endpoints

### Core Tables

### Channels

**users**- `GET /api/channels/` - List all channels

- User accounts, profiles, and authentication- `POST /api/channels/` - Create a new channel

- Fields: id, username, email, full_name, profile_pic, status, is_online- `GET /api/channels/{name}` - Get channel by name

- `PUT /api/channels/{channel_id}` - Update channel

**channels**- `DELETE /api/channels/{channel_id}` - Delete channel

- Public and private channels

- Fields: id, name, description, is_private, created_at### Messages

- `GET /api/messages/channel/{channel_id}` - Get channel messages

**channel_members**- `POST /api/messages/` - Send a message

- Many-to-many relationship between users and channels- `PUT /api/messages/{message_id}` - Edit message

- Fields: user_id, channel_id, joined_at- `DELETE /api/messages/{message_id}` - Delete message



**messages**### Direct Messages

- Channel messages- `GET /api/direct-messages/` - List all DM conversations

- Fields: id, content, sender_id, channel_id, created_at, updated_at- `GET /api/direct-messages/conversation/{user_id}` - Get DM thread

- `POST /api/direct-messages/` - Send a DM

**direct_messages**

- One-on-one conversations### Canvas

- Fields: id, content, sender_id, receiver_id, created_at- `GET /api/canvas/` - List all canvases

- `POST /api/canvas/` - Create a canvas

**canvas**- `GET /api/canvas/{canvas_id}` - Get canvas by ID

- Collaborative canvas documents- `PUT /api/canvas/{canvas_id}` - Update canvas

- Fields: id, title, content (JSON), channel_id, owner_id, is_public

### Attachments

**attachments**- `POST /api/attachments/` - Upload a file

- File uploads and metadata- `GET /api/attachments/` - List all attachments

- Fields: id, file_name, file_path, file_size, file_type, uploader_id- `GET /api/attachments/{attachment_id}` - Get file metadata



## 🧪 Sample Data## 🧪 Sample Data



The application comes pre-loaded with sample data:The application comes with sample data including:

- 5 demo users

**Users:**- 3 public channels (#general, #random, #development)

- alice@example.com (Alice Johnson)- Sample messages and conversations

- bob@example.com (Bob Smith)- Demo canvas documents

- charlie@example.com (Charlie Brown)

- diana@example.com (Diana Prince)## 🔐 Authentication

- eve@example.com (Eve Davis)

**Note**: Authentication is currently disabled for demo purposes. In production, you should:

**Channels:**1. Enable the authentication system in `App.jsx`

- #general - Main discussion channel2. Uncomment the authentication routes

- #random - For off-topic conversations3. Use JWT tokens for API authentication

- #development - Technical discussions4. Implement proper password hashing and validation



**Features:**## 🚧 Known Limitations

- Pre-populated messages in channels

- Sample direct message conversations- Real-time updates require WebSocket implementation (currently using polling)

- Demo canvas documents- File storage is local (consider cloud storage for production)

- Example file attachments- No message threading support yet

- Limited emoji reactions

## 📝 API Documentation- No video/voice call integration



### Interactive Documentation## 🔮 Future Enhancements



Once the backend is running:- [ ] WebSocket support for real-time updates

- **Swagger UI**: http://localhost:8000/docs- [ ] Message threading and replies

- **ReDoc**: http://localhost:8000/redoc- [ ] Advanced search with filters

- [ ] User presence and status

### Key Endpoints- [ ] Video/audio calls

- [ ] Screen sharing

**Channels:**- [ ] App integrations and bots

- `GET /api/channels/` - List all channels- [ ] Message formatting (code blocks, quotes)

- `POST /api/channels/` - Create channel- [ ] Notification system

- `GET /api/channels/{name}` - Get channel details- [ ] Mobile app



**Messages:**## 🤝 Contributing

- `GET /api/messages/channel/{id}` - Get channel messages

- `POST /api/messages/` - Send messageThis project was created for the ScalerAI Hackathon. Contributions are welcome!

- `PUT /api/messages/{id}` - Edit message

## 📄 License

**Direct Messages:**

- `GET /api/direct-messages/` - List conversationsMIT License - feel free to use this project for learning and development.

- `GET /api/direct-messages/conversation/{user_id}` - Get DM thread

- `POST /api/direct-messages/` - Send DM---



**Canvas:****Built with ❤️ for the ScalerAI Hackathon**

- `GET /api/canvas/` - List canvases
- `POST /api/canvas/` - Create canvas
- `PUT /api/canvas/{id}` - Update canvas

**Files:**
- `POST /api/attachments/` - Upload file
- `GET /api/attachments/` - List files
- `GET /api/attachments/{id}/download` - Download file

See [API.md](API.md) for complete API documentation.

## 🔧 Configuration

### Environment Variables

**Backend** (`.env` in `backend/` directory):
```env
DATABASE_URL=sqlite:///./slack.db
SECRET_KEY=your-secret-key-change-in-production
```

**Frontend** (`.env` in `frontend/` directory):
```env
VITE_API_URL=http://localhost:8000
```

## 🎨 Design Highlights

### Visual Fidelity
- Pixel-perfect recreation of Slack's UI design
- Consistent color scheme and typography
- Smooth hover effects and transitions
- Professional iconography

### User Experience
- Intuitive navigation patterns
- Real-time feedback for user actions
- Keyboard shortcuts support
- Loading states and error handling
- Responsive layout for all screen sizes

### Performance
- Optimized re-renders with React hooks
- Lazy loading for images and components
- Efficient state management
- Debounced auto-save for canvas
- Cached API responses

## 🚧 Known Limitations

- Real-time updates use polling instead of WebSockets
- File storage is local (not cloud-based)
- No message threading/replies yet
- Limited emoji reactions
- No video/voice call integration
- Authentication disabled for demo purposes

## 🔮 Future Enhancements

- [ ] WebSocket integration for true real-time updates
- [ ] Message threading and replies
- [ ] Advanced search with filters and operators
- [ ] User presence indicators
- [ ] Video and audio calls
- [ ] Screen sharing
- [ ] Slack app integrations and bots
- [ ] Code block syntax highlighting
- [ ] Push notifications
- [ ] Mobile applications (React Native)
- [ ] Multi-workspace support
- [ ] Message reactions and polls
- [ ] Scheduled messages
- [ ] Message bookmarks

## 🧪 Testing

### Manual Testing
1. Start the application using Docker
2. Navigate to http://localhost:5173
3. Test key features:
   - Send messages in #general channel
   - Create a new channel
   - Start a direct message conversation
   - Upload a file
   - Create and edit a canvas
   - Star channels and messages

### API Testing
Use the Swagger UI at http://localhost:8000/docs to test API endpoints

## 📚 Additional Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup and troubleshooting guide
- **[API.md](API.md)** - Complete API reference with examples
- **Backend Docs** - http://localhost:8000/docs (when running)

## 🤝 Contributing

This project was created for the ScalerAI Hackathon. 

### Development Workflow
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - Feel free to use this project for learning and development.

## 👥 Author

**ScalerAI Hackathon Submission**

GitHub Collaborator: [@raun](https://github.com/raun)

---

## 🙏 Acknowledgments

- **ScalerAI** for organizing the hackathon
- **Slack** for design inspiration
- **FastAPI** and **React** communities for excellent documentation

---

**Built with ❤️ for the ScalerAI Hackathon - Demonstrating fullstack development expertise through a high-fidelity Slack clone**
