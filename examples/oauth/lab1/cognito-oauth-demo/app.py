from flask import Flask, render_template, redirect, request, jsonify, session
import requests
import base64
import secrets
import urllib.parse

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

COGNITO_DOMAIN = 'https://oauth-lab1-920372995331-domain.auth.us-east-1.amazoncognito.com'
CLIENT_ID = '1nau172bra5rkpejavfj2ruvv3'
CLIENT_SECRET = '1bta25crkldftvqfuc40bc1kv48vtlfjs476a5kbh47nmvsptu8b'
REDIRECT_URI = 'http://localhost:5000/callback'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    # Generate and store state parameter
    state = secrets.token_hex(16)
    session['oauth_state'] = state
    
    # Construct authorization URL
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'scope': 'openid email profile',
        'redirect_uri': REDIRECT_URI,
        'state': state
    }
    auth_url = f"{COGNITO_DOMAIN}/oauth2/authorize?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route('/callback')
def callback():
    # Verify state parameter
    if request.args.get('state') != session.get('oauth_state'):
        return 'Invalid state parameter', 400
    
    # Exchange authorization code for tokens
    code = request.args.get('code')
    token_url = f"{COGNITO_DOMAIN}/oauth2/token"
    
    # Prepare Basic Auth header
    auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode('utf-8')).decode('utf-8')
    
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
    
    if response.status_code == 200:
        tokens = response.json()
        return f'''
            <script>
                sessionStorage.setItem('access_token', '{tokens["access_token"]}');
                window.location.href = '/';
            </script>
        '''
    return 'Error getting tokens', 400

@app.route('/userinfo')
def userinfo():
    # Get the access token from the Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return 'Missing or invalid Authorization header', 401
    
    access_token = auth_header.split(' ')[1]
    
    # Call Cognito userinfo endpoint
    userinfo_url = f"{COGNITO_DOMAIN}/oauth2/userInfo"
    response = requests.get(
        userinfo_url,
        headers={'Authorization': f'Bearer {access_token}'}
    )
    
    if response.status_code == 200:
        return jsonify(response.json())
    return 'Error getting user info', 400

if __name__ == '__main__':
    app.run(debug=True)
