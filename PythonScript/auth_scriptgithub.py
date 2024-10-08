from flask import Flask, redirect, request, session, jsonify
import requests
import os

app = Flask(__name__)
app.secret_key = 'admin'

GITHUB_CLIENT_ID = 'Ov23liZYIDywr2UvtYHk'
GITHUB_CLIENT_SECRET = '4b9bae658b73c61d4282efbcc347f85c308df7d9'
REDIRECT_URI = 'http://localhost:5000/callback' 
# GRAILS_APP_URL = 'http://localhost:8080/auth/validateToken'
GRAILS_APP_URL = 'http://localhost:4200/dashboard'

@app.route('/')
def index():
    return 'GitHub OAuth for Grails'

@app.route('/login')
def login():
    github_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={REDIRECT_URI}"
    return redirect(github_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    
    token_url = "https://github.com/login/oauth/access_token"
    token_payload = {
        'client_id': GITHUB_CLIENT_ID,
        'client_secret': GITHUB_CLIENT_SECRET,
        'code': code
    }
    headers = {'Accept': 'application/json'}
    token_response = requests.post(token_url, json=token_payload, headers=headers)
    token_json = token_response.json()

    access_token = token_json.get('access_token')

    user_url = "https://api.github.com/user"
    user_response = requests.get(user_url, headers={
        'Authorization': f'token {access_token}'
    })
    user_data = user_response.json()

    if user_data.get('login'):
        session['github_user'] = user_data
        return redirect(f'{GRAILS_APP_URL}?token={access_token}')
    else:
        return 'GitHub Authentication failed', 401

@app.route('/logout')
def logout():
    session.pop('github_user', None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
