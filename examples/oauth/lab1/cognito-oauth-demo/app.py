from flask import Flask, render_template, redirect, request, jsonify, session, make_response, send_from_directory
import requests
import base64
import secrets
import urllib.parse
import logging
import sys
import os
from flask_cors import CORS
from functools import wraps

# Configure logging to output to console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Test log
logger.debug("Starting application...")

# Get the absolute path of the directory containing app.py
app_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.join(app_dir, 'static')
templates_dir = os.path.join(app_dir, 'templates')

app = Flask(__name__,
           static_folder=static_dir,
           static_url_path='/static',
           template_folder=templates_dir)

# Configure CORS
CORS(app, resources={
    r"/*": {
        "origins": ["http://localhost:8080"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

app.secret_key = secrets.token_hex(16)

logger.debug(f"Static folder: {static_dir}")
logger.debug(f"Template folder: {templates_dir}")
logger.debug("Initialized Flask application")

COGNITO_DOMAIN = 'https://oauth-lab1-920372995331-domain.auth.us-east-1.amazoncognito.com'
CLIENT_ID = '1nau172bra5rkpejavfj2ruvv3'
CLIENT_SECRET = '1bta25crkldftvqfuc40bc1kv48vtlfjs476a5kbh47nmvsptu8b'
REDIRECT_URI = 'http://localhost:8080/callback'
APP_URL = 'http://localhost:8080'

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:8080')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

@app.route('/')
def index():
    logger.info('=== Handling request to index page ===')
    logger.debug('Session data: %s', dict(session))
    return render_template('index.html')

@app.route('/login')
def login():
    logger.info('=== Starting login process ===')
    state = secrets.token_hex(16)
    session['oauth_state'] = state
    logger.debug('Generated state: %s', state)

    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': 'openid email profile',
        'redirect_uri': REDIRECT_URI,
        'state': state
    }
    auth_url = f"{COGNITO_DOMAIN}/oauth2/authorize?{urllib.parse.urlencode(params)}"
    logger.debug('Generated authorization URL: %s', auth_url)
    return redirect(auth_url)

@app.route('/callback')
def callback():
    logger.info('=== Received callback ===')
    logger.debug('Query parameters: %s', dict(request.args))
    logger.debug('Session data: %s', dict(session))

    # Check for error in callback
    if 'error' in request.args:
        error = request.args.get('error')
        error_description = request.args.get('error_description', '')
        logger.error('Error in callback: %s - %s', error, error_description)
        return f'Error: {error} - {error_description}', 400

    received_state = request.args.get('state')
    stored_state = session.get('oauth_state')
    logger.debug('State comparison - Received: %s, Stored: %s', received_state, stored_state)

    if received_state != stored_state:
        logger.error('State parameter mismatch')
        return 'Invalid state parameter', 400

    code = request.args.get('code')
    logger.debug('Received authorization code: %s', code)

    token_url = f"{COGNITO_DOMAIN}/oauth2/token"
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode('utf-8')).decode('utf-8')

    try:
        logger.info('=== Exchanging code for tokens ===')
        response = requests.post(
            token_url,
            headers={
                'Authorization': f'Basic {auth_header}',
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': REDIRECT_URI
            }
        )

        logger.debug('Token endpoint response - Status: %s', response.status_code)
        logger.debug('Token endpoint response - Headers: %s', dict(response.headers))
        logger.debug('Token endpoint response - Body: %s', response.text)

        if response.status_code == 200:
            tokens = response.json()
            logger.info('Successfully obtained tokens')
            html_response = make_response(f'''
                <html>
                <body>
                    <script>
                        console.log('Setting access token in session storage');
                        window.sessionStorage.setItem('access_token', '{tokens["access_token"]}');
                        console.log('Redirecting to main page');
                        window.location.href = '{APP_URL}';
                    </script>
                </body>
                </html>
            ''')
            return html_response
        else:
            logger.error('Token endpoint error: %s - %s', response.status_code, response.text)
            return f'Error getting tokens: {response.text}', 400
    except Exception as e:
        logger.exception('Exception during token exchange')
        return f'Error during token exchange: {str(e)}', 500

@app.route('/userinfo')
def userinfo():
    logger.info('=== Handling userinfo request ===')
    auth_header = request.headers.get('Authorization')
    logger.debug('Authorization header: %s', auth_header)

    if not auth_header or not auth_header.startswith('Bearer '):
        logger.error('Missing or invalid Authorization header')
        return 'Missing or invalid Authorization header', 401

    access_token = auth_header.split(' ')[1]
    logger.debug('Extracted access token')

    try:
        userinfo_url = f"{COGNITO_DOMAIN}/oauth2/userInfo"
        logger.info('Calling userinfo endpoint: %s', userinfo_url)

        response = requests.get(
            userinfo_url,
            headers={'Authorization': f'Bearer {access_token}'}
        )

        logger.debug('Userinfo response - Status: %s', response.status_code)
        logger.debug('Userinfo response - Headers: %s', dict(response.headers))
        logger.debug('Userinfo response - Body: %s', response.text)

        if response.status_code == 200:
            user_data = response.json()
            logger.info('Successfully retrieved user info')
            return jsonify(user_data)
        else:
            logger.error('Userinfo endpoint error: %s - %s', response.status_code, response.text)
            return f'Error getting user info: {response.text}', 400
    except Exception as e:
        logger.exception('Exception during userinfo request')
        return f'Error fetching user info: {str(e)}', 500

if __name__ == '__main__':
    logger.info('=== Starting Flask application ===')
    app.run(host='0.0.0.0', port=8080, debug=True)
