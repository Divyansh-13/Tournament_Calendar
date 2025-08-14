# 🏆 Sports Event Aggregator

> AI-powered real-time sports tournament discovery platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI%20Powered-purple.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 Overview

Sports Event Aggregator is an intelligent platform that discovers and aggregates upcoming sports tournaments across multiple levels - from local school competitions to international championships. Powered by Google's Gemini AI, it provides real-time tournament data with comprehensive details including dates, streaming information, and official links.

## 🎥 Demo Video

[Click here to watch the demo](https://drive.google.com/file/d/1YoMKLuBGKHaWB5AnITHtv4jvDnnGXaf3/view?usp=sharing)



## ✨ Features

### 🔍 *Smart Tournament Discovery*
- AI-powered search across multiple sports
- Real-time data aggregation from various sources
- Comprehensive tournament categorization

### 🏅 *Multi-Level Coverage*
- *Corporate* tournaments and leagues
- *School & College* competitions  
- *Club & Academy* events
- *District & State* championships
- *Zonal & Regional* competitions
- *National* tournaments
- *International* championships

### 📱 *Modern Web Interface*
- Responsive design for all devices
- Intuitive sport selection interface
- Real-time IST clock display
- Beautiful gradient UI with smooth animations

### 🚀 *Robust Architecture*
- Flask-based REST API
- Fallback system with mock data
- Comprehensive error handling
- CORS enabled for cross-origin requests

## 🛠 Tech Stack

- *Backend:* Flask (Python)
- *AI Engine:* Google Gemini 2.0 Flash
- *Frontend:* Vanilla HTML5/CSS3/JavaScript
- *Styling:* Custom CSS with modern gradients
- *Icons:* Font Awesome 6.0
- *Timezone:* Asia/Kolkata (IST)

## 🏃‍♂ Quick Start

### Prerequisites
- Python 3.8+
- Google Gemini API Key

### Installation

1. *Clone the repository*
   bash
   git clone https://github.com/Divyansh-13/Tournament_Calendar.git
   cd sports-event-aggregator
   

2. *Install dependencies*
   bash
   pip install flask flask-cors requests pytz
   

3. *Set up environment variables*
   bash
   export GEMINI_API_KEY="your-gemini-api-key-here"
   

4. *Run the application*
   bash
   python app.py
   

5. *Access the app*
   
   http://localhost:5000
   

## 🎮 Usage

### Web Interface
1. Open the application in your browser
2. Select any sport from the beautiful card interface
3. View real-time tournament data with comprehensive details
4. Click on official links to visit tournament websites
5. Check streaming partners for live coverage information

### API Endpoints

#### Get Available Sports
http
GET /api/sports


#### Get Tournaments for Specific Sport
http
GET /api/tournaments/{sport}


#### Health Check
http
GET /api/health


### Example Response
json
{
  "success": true,
  "sport": "badminton",
  "tournaments": [
    {
      "tournament_name": "BWF World Championships 2025",
      "level": "International",
      "start_date": "2025-10-10",
      "end_date": "2025-10-17",
      "official_url": "https://bwfbadminton.com/tournament",
      "streaming_partners": ["Olympic Channel", "BWF TV"],
      "summary": "World's premier badminton championship with players from over 50 countries."
    }
  ],
  "count": 1,
  "mode": "api"
}


## 🏗 Project Structure


sports-event-aggregator/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Frontend interface
├── requirements.txt      # Python dependencies
├── README.md            # Project documentation
└── .env.example         # Environment variables template


## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| GEMINI_API_KEY | Google Gemini API key | Yes |

### Supported Sports

- 🏏 Cricket
- ⚽ Football  
- 🏸 Badminton
- 🏃‍♂ Running
- 💪 Gym
- 🚴‍♂ Cycling
- 🏊‍♂ Swimming
- 🤼‍♂ Kabaddi
- 🧘‍♀ Yoga
- 🏀 Basketball
- ♟ Chess
- 🏓 Table Tennis

## 📊 Features in Detail

### AI-Powered Data Aggregation
The system uses Google's Gemini 2.0 Flash model to intelligently search and extract tournament information from various sources, ensuring accuracy and comprehensiveness.

### Fallback System
- *Primary:* Gemini AI API for real-time data
- *Secondary:* Mock data system for development/testing
- *Tertiary:* Error handling with graceful degradation

### Modern UI/UX
- Gradient backgrounds and smooth animations
- Hover effects and interactive elements
- Mobile-responsive design
- Real-time IST clock display

## 🚀 Deployment

### Local Development
bash
python app.py


### Production Deployment
1. Set production environment variables
2. Use a production WSGI server like Gunicorn
3. Configure reverse proxy (nginx)
4. Set up SSL certificates

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request


## 🙏 Acknowledgments

- Google Gemini AI for intelligent data aggregation
- Font Awesome for beautiful icons
- Flask community for the robust web framework
- All sports organizations for making tournament data accessible


---

<div align="center">
  <p>Made with ❤ for sports enthusiasts worldwide</p>
  <p>⭐ Star this repo if you found it helpful!</p>
</div>
