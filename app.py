from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import json
from datetime import datetime
import pytz
import os
from typing import List, Dict, Any
import logging
import re

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL= 'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent'

if GEMINI_API_KEY == 'GEMINI_API_KEY':
    logger.warning("Gemini API key not properly configured. Using mock data mode.")

class SportsAggregator:
    def __init__(self):
        self.indian_tz = pytz.timezone('Asia/Kolkata')
        self.current_date = datetime.now(self.indian_tz).strftime('%Y-%m-%d')
        
    def create_gemini_prompt(self, sport: str) -> str:
        """Create the prompt for Gemini API"""
        return f"""You are an expert sports event aggregator assistant.
Search on your own but data has to be perfect and absolutely correct raw textual data about upcoming sports tournaments in {sport} across multiple levels: Corporate, School, College/University, Club/Academy, District, State, Zonal/Regional, National, International.

Your task:
Extract the tournament details:
- Tournament Name
- Level (one of the specified levels)
- Start Date (ISO format: YYYY-MM-DD)
- End Date (ISO format)
- Official Tournament URL
- Streaming Partners or Streaming Links (if available)
- Tournament Image URL (if available)
- A brief summary (max 50 words) describing the tournament, its significance, and scope.

Format your output strictly as a JSON array of objects with these fields.
Ensure the data is accurate, no fabricated information. If some data fields are missing, use null or empty string.

Example:
[
{{
"tournament_name": "Asian Badminton Championship 2025",
"level": "International", 
"start_date": "2025-09-10",
"end_date": "2025-09-18",
"official_url": "https://asianbadminton2025.org",
"streaming_partners": ["Hotstar", "YouTube"],
"tournament_image": "https://asianbadminton2025.org/banner.jpg",
"summary": "A prestigious continental championship featuring top Asian badminton players."
}}
]

Give real time data in Indian time zone for today's date: {self.current_date}. Focus on tournaments starting from today onwards."""

    def get_mock_data(self, sport: str) -> List[Dict[str, Any]]:
        """Return mock tournament data for testing when API is not available"""
        mock_tournaments = {
            'badminton': [
                {
                    "tournament_name": f"All India {sport.capitalize()} Championship 2025",
                    "level": "National",
                    "start_date": "2025-09-15",
                    "end_date": "2025-09-22",
                    "official_url": "https://badmintonindia.org/tournament",
                    "streaming_partners": ["Star Sports", "Hotstar"],
                    "tournament_image": None,
                    "summary": f"Premier national {sport} championship featuring top players from across India."
                },
                {
                    "tournament_name": f"BWF World {sport.capitalize()} Championships",
                    "level": "International",
                    "start_date": "2025-10-10",
                    "end_date": "2025-10-17",
                    "official_url": "https://bwfbadminton.com/tournament",
                    "streaming_partners": ["Olympic Channel", "BWF TV"],
                    "tournament_image": None,
                    "summary": f"World's premier {sport} championship with players from over 50 countries."
                }
            ],
            'tennis': [
                {
                    "tournament_name": f"Indian {sport.capitalize()} Open 2025",
                    "level": "National",
                    "start_date": "2025-09-20",
                    "end_date": "2025-09-27",
                    "official_url": "https://tennisindiaopen.com",
                    "streaming_partners": ["Sony Sports"],
                    "tournament_image": None,
                    "summary": f"Major {sport} tournament featuring international and domestic players."
                }
            ]
        }
        
        return mock_tournaments.get(sport.lower(), [
            {
                "tournament_name": f"National {sport.capitalize()} Championship 2025",
                "level": "National",
                "start_date": "2025-09-25",
                "end_date": "2025-09-30",
                "official_url": None,
                "streaming_partners": [],
                "tournament_image": None,
                "summary": f"Annual national championship for {sport} featuring top athletes."
            }
        ])

    def query_gemini(self, prompt: str) -> Dict[str, Any]:
        """Query Gemini API with the given prompt"""
        if GEMINI_API_KEY == 'your-gemini-api-key-here':
            logger.info("Using mock data due to missing API key")
            return {'success': True, 'data': [], 'mock': True}
        
        headers = {
            'Content-Type': 'application/json',
        }
        
        data = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': prompt
                        }
                    ]
                }
            ]
        }
        
        try:
            logger.info(f"Sending request to Gemini API with URL: {GEMINI_API_URL}")
            response = requests.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                headers=headers,
                json=data,
                timeout=30
            )
            
            logger.info(f"Gemini API response status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                logger.debug(f"Gemini API response: {result}")
                
                if 'candidates' in result and len(result['candidates']) > 0:
                    content = result['candidates'][0]['content']['parts'][0]['text']
                    logger.info(f"Received content from Gemini: {content[:200]}...")
                    
                    
                    try:
                    
                        content = content.strip()
                        
                
                        json_patterns = [
                            r'\[[\s\S]*?\]',  
                            r'```json\s*(\[[\s\S]*?\])\s*```',  
                            r'```\s*(\[[\s\S]*?\])\s*```'  
                        ]
                        
                        tournaments = []
                        for pattern in json_patterns:
                            matches = re.findall(pattern, content)
                            for match in matches:
                                try:
                                    if isinstance(match, tuple):
                                        match = match[0] if match[0] else match[1]
                                    parsed = json.loads(match)
                                    if isinstance(parsed, list):
                                        tournaments = parsed
                                        break
                                except json.JSONDecodeError:
                                    continue
                            if tournaments:
                                break
                        
                        if tournaments:
                            logger.info(f"Successfully parsed {len(tournaments)} tournaments")
                            return {'success': True, 'data': tournaments}
                        else:
                            logger.warning("No valid JSON array found in response")
                            return {'success': False, 'error': 'No valid JSON found in response', 'raw_content': content[:500]}
                            
                    except Exception as parse_error:
                        logger.error(f"JSON parsing error: {str(parse_error)}")
                        return {'success': False, 'error': f'Failed to parse JSON: {str(parse_error)}', 'raw_content': content[:500]}
                else:
                    logger.error("No candidates in Gemini response")
                    return {'success': False, 'error': 'No candidates in response', 'response': result}
            else:
                error_text = response.text
                logger.error(f"Gemini API error {response.status_code}: {error_text}")
                return {'success': False, 'error': f'API request failed: {response.status_code}', 'details': error_text}
                
        except requests.exceptions.Timeout:
            logger.error("Request timeout")
            return {'success': False, 'error': 'Request timeout - please try again'}
        except requests.exceptions.ConnectionError:
            logger.error("Connection error")
            return {'success': False, 'error': 'Connection error - please check your internet connection'}
        except requests.exceptions.RequestException as e:
            logger.error(f"Request exception: {str(e)}")
            return {'success': False, 'error': f'Network error: {str(e)}'}

sports_aggregator = SportsAggregator()

@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/tournaments/<sport>')
def get_tournaments(sport):
    """Get tournaments for a specific sport"""
    try:
        logger.info(f"Received request for {sport} tournaments")
        

        prompt = sports_aggregator.create_gemini_prompt(sport.capitalize())
        logger.debug(f"Created prompt for {sport}")
        
        if GEMINI_API_KEY == 'your-gemini-api-key-here':
            mock_data = sports_aggregator.get_mock_data(sport)
            logger.info(f"Using mock data for {sport}: {len(mock_data)} tournaments")
            return jsonify({
                'success': True,
                'sport': sport,
                'tournaments': mock_data,
                'fetched_at': datetime.now(sports_aggregator.indian_tz).isoformat(),
                'count': len(mock_data),
                'mode': 'mock'
            })
        else:
    
            result = sports_aggregator.query_gemini(prompt)
            logger.info(f"Gemini API result: {result.get('success', False)}")
            
            if result['success']:
                tournaments = result['data']
                logger.info(f"Successfully fetched {len(tournaments)} tournaments for {sport}")
                return jsonify({
                    'success': True,
                    'sport': sport,
                    'tournaments': tournaments,
                    'fetched_at': datetime.now(sports_aggregator.indian_tz).isoformat(),
                    'count': len(tournaments),
                    'mode': 'api'
                })
            else:
            
                logger.warning(f"API failed for {sport}, using mock data. Error: {result.get('error')}")
                mock_data = sports_aggregator.get_mock_data(sport)
                return jsonify({
                    'success': True,
                    'sport': sport,
                    'tournaments': mock_data,
                    'fetched_at': datetime.now(sports_aggregator.indian_tz).isoformat(),
                    'count': len(mock_data),
                    'mode': 'fallback',
                    'api_error': result.get('error')
                })
            
    except Exception as e:
        logger.error(f"Unexpected error in get_tournaments: {str(e)}", exc_info=True)
    
        try:
            mock_data = sports_aggregator.get_mock_data(sport)
            return jsonify({
                'success': True,
                'sport': sport,
                'tournaments': mock_data,
                'fetched_at': datetime.now(sports_aggregator.indian_tz).isoformat(),
                'count': len(mock_data),
                'mode': 'error_fallback',
                'error': str(e)
            })
        except Exception as fallback_error:
            logger.error(f"Even fallback failed: {str(fallback_error)}")
            return jsonify({
                'success': False,
                'error': f'System error: {str(e)}',
                'sport': sport
            }), 500

@app.route('/api/sports')
def get_available_sports():
    """Get list of available sports"""
    sports_list = [
        'Cricket', 'Football', 'Badminton', 'Running', 'Gym', 'Cycling', 'Swimming', 'Kabaddi', 'Yoga', 'Basketball',
        'Chess', 'Table Tennis'
    ]
    return jsonify({
        'success': True,
        'sports': sports_list
    })

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now(sports_aggregator.indian_tz).isoformat(),
        'timezone': 'Asia/Kolkata'
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)