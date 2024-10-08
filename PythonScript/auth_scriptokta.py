from flask import Flask, redirect, request, session, jsonify
import requests
import os
import base64

app = Flask(__name__)
app.secret_key = 'admin'

# Use your Okta credentials here
OKTA_CLIENT_ID = '0oajqn02axBZ2NoU65d7'
OKTA_CLIENT_SECRET = 'C-3RTF2QhVwBi-hPu-V1wAY1PxnEUejiXZRUTx-vhwxvxegYUZEVMgQOJkUXen6S'
OKTA_REDIRECT_URI = 'http://localhost:5000/callback'
OKTA_DOMAIN = 'dev-80747872.okta.com'
OKTA_AUTH_SERVER_ID = 'default'
GRAILS_APP_URL = 'http://localhost:8080/auth/validateToken'

# Okta API URLs
AUTHORIZATION_URL = f"https://{OKTA_DOMAIN}/oauth2/{OKTA_AUTH_SERVER_ID}/v1/authorize"
TOKEN_URL = f"https://{OKTA_DOMAIN}/oauth2/{OKTA_AUTH_SERVER_ID}/v1/token"
USERINFO_URL = f"https://{OKTA_DOMAIN}/oauth2/{OKTA_AUTH_SERVER_ID}/v1/userinfo"

@app.route('/')
def index():
    return 'Okta OAuth for Grails'

@app.route('/login')
def login():
    # Generate random state and store in session to prevent CSRF attacks
    state = base64.urlsafe_b64encode(os.urandom(30)).decode('utf-8')
    session['oauth_state'] = state

    # Redirect the user to Okta for authentication
    authorization_url = (
        f"{AUTHORIZATION_URL}"
        f"?client_id={OKTA_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid profile email"
        f"&redirect_uri={OKTA_REDIRECT_URI}"
        f"&state={state}"
    )
    return redirect(authorization_url)

@app.route('/callback')
def callback():
    # Verify the state parameter to prevent CSRF attacks
    state = request.args.get('state')
    if state != session.get('oauth_state'):
        return 'Invalid state parameter', 400

    code = request.args.get('code')
    if not code:
        return 'No authorization code received', 400

    # Exchange the authorization code for an access token
    token_payload = {
        'client_id': OKTA_CLIENT_ID,
        'client_secret': OKTA_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'redirect_uri': OKTA_REDIRECT_URI,
        'code': code
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    token_response = requests.post(TOKEN_URL, data=token_payload, headers=headers)
    if token_response.status_code != 200:
        return f"Error getting access token: {token_response.text}", 400

    token_json = token_response.json()
    access_token = token_json.get('access_token')
    if not access_token:
        return 'Failed to get access token', 400

    # Fetch user info from Okta using the access token
    userinfo_response = requests.get(USERINFO_URL, headers={
        'Authorization': f'Bearer {access_token}'
    })
    user_data = userinfo_response.json()
    if 'error' in user_data:
        return f"Error fetching user info: {userinfo_response.text}", 400

    # Save user data in session
    session['okta_user'] = user_data

    # Send access token to Grails app via Authorization header (recommended)
    headers = {'Authorization': f'Bearer {access_token}'}
    grails_response = requests.get(GRAILS_APP_URL, headers=headers)
    return grails_response.text

@app.route('/logout')
def logout():
    session.pop('okta_user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
