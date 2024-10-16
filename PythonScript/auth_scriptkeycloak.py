from flask import Flask, redirect, request, session, jsonify
import requests

app = Flask(__name__)
app.secret_key = 'admin'

# Keycloak Configuration
KEYCLOAK_CLIENT_ID = 'icoraltest-keycloak'
KEYCLOAK_CLIENT_SECRET = 'Wfc0RTW7ZZXnJ6gB7FW9XtHzUO0PbqlM'
KEYCLOAK_HOST = 'http://localhost:8080'  # Keycloak host URL
REALM_NAME = 'icoraltest'  # Your correct Keycloak realm name
REDIRECT_URI = 'http://localhost:5000/callback'  # Should match your Keycloak client config
GRAILS_APP_URL = 'http://localhost:4200/dashboard'

# Keycloak Endpoints
AUTHORIZATION_URL = f"{KEYCLOAK_HOST}/realms/{REALM_NAME}/protocol/openid-connect/auth"
TOKEN_URL = f"{KEYCLOAK_HOST}/realms/{REALM_NAME}/protocol/openid-connect/token"
USER_INFO_URL = f"{KEYCLOAK_HOST}/realms/{REALM_NAME}/protocol/openid-connect/userinfo"

@app.route('/')
def index():
    return 'Keycloak OAuth for Grails'

@app.route('/login')
def login():
    keycloak_url = (
        f"{AUTHORIZATION_URL}?client_id={KEYCLOAK_CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}&response_type=code&scope=openid"
    )
    return redirect(keycloak_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    # Exchange authorization code for access token
    token_payload = {
        'client_id': KEYCLOAK_CLIENT_ID,
        'client_secret': KEYCLOAK_CLIENT_SECRET,
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    
    token_response = requests.post(TOKEN_URL, data=token_payload, headers=headers)
    
    # Check if the token response is successful
    if token_response.status_code != 200:
        return 'Token exchange failed', 401

    token_json = token_response.json()
    access_token = token_json.get('access_token')

    if not access_token:
        return 'Token exchange failed', 401

    # Fetch user info from Keycloak using the access token
    user_response = requests.get(USER_INFO_URL, headers={
        'Authorization': f'Bearer {access_token}'
    })

    # Check if the user response is successful
    if user_response.status_code != 200:
        return 'Failed to fetch user info', 401

    user_data = user_response.json()

    if user_data.get('preferred_username'):
        session['keycloak_user'] = user_data
        return redirect(f'{GRAILS_APP_URL}?token={access_token}')
    else:
        return 'Keycloak Authentication failed', 401

@app.route('/logout')
def logout():
    session.pop('keycloak_user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
