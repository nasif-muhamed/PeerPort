# PeerPort 💬

A real-time temporary chat room application built with modern web technologies, enabling users to create, join and destroy ephemeral chat rooms with dynamic participant management.

## ✨ Features

### Core Functionality
- **Temporary Chat Rooms**: Create chat rooms with customizable participant limits
- **Real-time Communication**: Instant messaging powered by WebSocket technology
- **Public Room Discovery**: Browse all active rooms in a centralized room list
- **Seamless Join/Leave**: Users can freely join and leave rooms without restrictions

### Room Management
- **Room Creation**: Any user can create a new temporary chat room
- **Dynamic Room Control**: Room owners can:
  - Update room name and description
  - Set room status (Active/Inactive)
  - Modify participant limits
  - View and manage participant lists
  - Delete rooms entirely at any time

### User Experience
- **Responsive Design**: Optimized for both desktop and mobile devices
- **Real-time Updates**: Live participant count and room status updates
- **Intuitive Interface**: Clean, user-friendly React-based frontend

## 🛠️ Tech Stack

### Backend
- **Django**: Robust Python web framework
- **Django REST Framework (DRF)**: API development and serialization
- **Django Channels**: WebSocket support for real-time communication
- **WebSocket**: Bi-directional real-time communication protocol

### Frontend
- **React**: Modern JavaScript library for building user interfaces
- **WebSocket Client**: Real-time communication with the backend

### Infrastructure
- **ASGI**: Asynchronous Server Gateway Interface for handling WebSocket connections
- **Redis** (recommended): Channel layer backend for production deployment

## 🚀 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Redis (for production)

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/nasif-muhamed/PeerPort.git
cd PeerPort
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure database**
```bash
python manage.py migrate
```

5. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

6. **Start the Django development server**
```bash
python manage.py runserver
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend  # Adjust path as needed
```

2. **Install Node.js dependencies**
```bash
npm install
```

3. **Start the React development server**
```bash
npm start
```

### Environment Variables

Create a `.env` file in the project \server:

```env
DEBUG="True"
SECRET_KEY=your-"django-secret-key-here"
DJANGO_LOG_LEVEL="DEBUG"
ALLOWED_HOSTS="localhost,127.0.0.1"
CORS_ALLOWED_ORIGINS="http://localhost:5173,http://127.0.0.1:5173
REFRESH_TOKEN_LIFETIME="your_refresh_token_lifetime_in_days"
ACCESS_TOKEN_LIFETIME="your_access_token_lifetime_in_minutes"
JWT_SECRET_KEY="your_jwt_secret_key"
JWT_ALGORITHM="your_jwt_algorithm"

# Database Configuration
DB_ENGINE="your_db_engin"
DB_NAME="your_db_name"
DB_USER="your_db_user"
DB_PASSWORD="your_db_password"
DB_HOST="your_db_host"
DB_PORT="your_db_port"

# Optional - Redis Configuration (for production)
REDIS_URL=redis://localhost:6379/0
```
Create a `.env` file in the project \client:

```env
VITE_APP_DEBUG="true"
VITE_API_URL="http://localhost:8000"
VITE_WS_BASE_URL="ws://localhost:8000"
```

## 📋 API Endpoints

### Rooms
- `GET /api/rooms/` - List all active rooms
- `POST /api/rooms/` - Create a new room
- `GET /api/rooms/{id}/` - Get room details
- `PUT/PATCH /api/rooms/{id}/` - Update room (owner only)
- `DELETE /api/rooms/{id}/` - Delete room (owner only)

### Participants
- `GET /api/rooms/{id}/participants/` - List room participants
- `POST /api/rooms/{id}/join/` - Join a room
- `POST /api/rooms/{id}/leave/` - Leave a room

### WebSocket Endpoints
- `ws://localhost:8000/ws/room/{room_id}/` - Room chat WebSocket

## 🔮 Future Roadmap

### Upcoming Features

#### Private Rooms
- **Request-Based Access**: Room owners can approve/deny join requests
- **Invitation System**: Send direct invitations to specific users
- **Access Control**: Enhanced privacy settings for sensitive discussions

#### Advanced Participant Management
- **Persistent Participants**: Maintain participant history across sessions
- **Moderation Tools**: Admin ability to remove disruptive participants
- **Role-Based Permissions**: Different user roles with varying capabilities

#### Video Communication
- **Peer-to-Peer Video Rooms**: WebRTC integration for video calls
- **Screen Sharing**: Share screens during video sessions
- **Audio/Video Controls**: Mute/unmute and camera on/off functionality

#### Enhanced Features
- **Message History**: Optional message persistence for active rooms
- **File Sharing**: Upload and share files within chat rooms
- **Emoji Reactions**: React to messages with emojis
- **User Profiles**: Basic user profile management

## 🏗️ Project Structure

```
PeerPort/
├── backend/
│   ├── chat/           # Chat application
│   ├── rooms/          # Room management
│   └── settings/       # Django settings
├── frontend/
│   ├── src/
│   │   ├── components/ # React components
│   │   ├── pages/      # Application pages
│   │   └── services/   # API services
│   └── public/
└── README.md          # This file
```

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 👨‍💻 Author

**Muhamed Nasif**
- GitHub: [@nasif-muhamed](https://github.com/nasif-muhamed)

## 🙏 Acknowledgments

- Django Channels team for excellent WebSocket support
- React community for the amazing frontend framework

---

**⭐ If you find this project useful, please give it a star!**
