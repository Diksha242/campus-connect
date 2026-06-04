🎓 Campus Connect
A full-featured Django-based college social platform that brings campus life online — students can connect, share posts, join clubs, attend events, trade items, and manage everything related to campus in one place.

🚀 Live Demo

🔗 Coming soon — deploying on Railway


📸 Screenshots

(Add screenshots of your feed, profile, marketplace, and events pages here)


✨ Features
ModuleDescription🔐 AuthenticationSignup, login, logout with session management👤 User ProfilesBio, profile picture, department, year, interests👥 Follow SystemFollow / unfollow users, followers and following lists📰 Social FeedCreate posts with images, like, comment, delete💬 Direct MessagingReal-time chat UI between users🔔 NotificationsAlerts for likes, comments, follows, messages, events📅 EventsCreate events with date, location, capacity — RSVP system🏛️ ClubsCreate and join college clubs, view member lists🛒 MarketplaceBuy and sell books, electronics, clothes, furniture, and more🔍 Lost & FoundPost lost or found items with status tracking🌐 DiscoveryFind and connect with students not yet followed📢 Student VoicePlatform for student opinions and announcements📚 ResourcesAcademic resources and links

🛠️ Tech Stack

Backend: Python, Django 5.2
Frontend: HTML5, CSS3, JavaScript
Database: SQLite (development) / PostgreSQL (production)
Media Handling: Pillow
Static Files: WhiteNoise
Deployment: Gunicorn, Railway / Render


📁 Project Structure
campus-connect/
├── campus_connect/        # Django project settings and URL routing
├── home/                  # Core app
│   ├── models.py          # All data models
│   ├── views.py           # Page logic and actions
│   └── urls.py            # App routes
├── templates/             # HTML templates
├── static/                # CSS, JS, static assets
├── media/                 # User uploaded images
├── requirements.txt       # Python dependencies
├── Procfile               # Deployment config
└── manage.py

⚙️ Getting Started
Prerequisites

Python 3.10+
pip

Installation
bash# Clone the repository
git clone https://github.com/Diksha242/campus-connect.git
cd campus-connect

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Apply migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser

# Run the development server
python manage.py runserver
Visit http://127.0.0.1:8000 in your browser.

🔗 URL Routes
RouteDescription/Home feed/signup/ /login/ /logout/Authentication/profile/<username>/User profile/create-post/New post/messages/ /chat/<username>/Messaging/events/ /create-event/Events/clubs/ /create-club/Clubs/marketplace/ /create-listing/Marketplace/lostfound/Lost & Found/notifications/Notifications