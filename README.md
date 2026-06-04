🎓 Campus Connect
A full-featured Django-based college social platform that brings campus life online  here students can connect, share posts, join clubs, attend events, trade items, and manage everything related to campus in one place.

 Live Demo

🔗 Coming soon — deploying on Render


# Features

### Secure Authentication

Users can create an account, log in, and log out securely. Session management ensures a smooth and safe experience across the platform.

### Personalized User Profiles

Every student gets a customizable profile where they can add a bio, upload a profile picture, specify their department and academic year, and share their interests.

### Connect with Other Students

Build your network by following classmates and discovering new people. Users can easily view their followers and the people they follow.

### Social Feed

Share updates, campus moments, and experiences through posts. Students can upload images, like posts, leave comments, and manage their own content.

### Direct Messaging

Communicate privately with other students through an intuitive real-time chat interface designed for quick and seamless conversations.

### Notifications

Stay informed with instant notifications for new followers, likes, comments, messages, event updates, and other important activities.

### Events Management

Create and promote college events by adding details such as date, location, and participant limits. Students can RSVP and keep track of upcoming activities.

### Student Clubs

Form communities around shared interests by creating clubs, joining existing ones, and exploring club member directories.

### Campus Marketplace

Buy and sell items within the student community, including books, electronics, furniture, clothing, and other essentials.

### Lost & Found

Help students recover misplaced belongings through dedicated lost-and-found listings with status tracking and updates.

### Student Discovery

Explore and connect with students across different departments and years, making it easier to expand your campus network.

### Student Voice

A space where students can share opinions, discuss ideas, make announcements, and engage in meaningful campus conversations.

### Academic Resources

Access and share useful study materials, educational links, academic resources, and learning opportunities with fellow students.

🛠️ Tech Stack

Backend: Python, Django 5.2
Frontend: HTML5, CSS3, JavaScript
Database: SQLite (development) / PostgreSQL (production)
Media Handling: Pillow
Static Files: WhiteNoise
Deployment: Gunicorn, Render


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
