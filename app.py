from flask import Flask, render_template, request, redirect, session, url_for
from database import create_connection, create_tables, register_user, authenticate_user, get_google_user, register_google_user, register_facebook_user, get_facebook_user, get_user_by_username
from config import SECRET_KEY, GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET, FACEBOOK_APP_ID, FACEBOOK_APP_SECRET
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from urllib.parse import urlencode
import requests

app = Flask(__name__)
app.secret_key = SECRET_KEY

# Facebook OAuth endpoints
FACEBOOK_AUTH_URL = 'https://www.facebook.com/dialog/oauth'
FACEBOOK_TOKEN_URL = 'https://graph.facebook.com/oauth/access_token'
FACEBOOK_USER_INFO_URL = 'https://graph.facebook.com/me'

@app.route('/')
def home():
    if 'username' in session:
        return f'Welcome, {session["username"]}!'
    return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if authenticate_user(username, password):
            session['username'] = username
            return redirect(url_for('welcome'))
        else:
            error = 'Invalid username or password'
            return render_template('login.html', error=error)
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if register_user(username, password):
            return redirect('/login')
        else:
            error = 'Username already exists'
    return render_template('register.html', error=error)

@app.route('/welcome')
def welcome():
    if 'username' in session:
        username = session['username']
        return render_template('welcome.html', username=username)
    return redirect(url_for('login'))

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/login/google')
def google_login():
    # Generate the Google OAuth authorization URL
    google_auth_url = f'https://accounts.google.com/o/oauth2/auth?client_id={GOOGLE_CLIENT_ID}&redirect_uri={url_for("google_callback", _external=True)}&response_type=code&scope=openid%20email%20profile&access_type=offline&prompt=consent'
    
    # Redirect the user to the Google OAuth authorization page
    return redirect(google_auth_url)

@app.route('/login/google/callback')
def google_callback():
    # Retrieve the authorization code from the request
    code = request.args.get('code')

    # Exchange the authorization code for an access token and refresh token
    token_url = 'https://oauth2.googleapis.com/token'
    token_payload = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': url_for('google_callback', _external=True),
        'grant_type': 'authorization_code'
    }
    token_response = requests.post(token_url, data=token_payload)
    token_data = token_response.json()

    # Retrieve the user's information using the access token
    access_token = token_data['access_token']
    userinfo_url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    headers = {'Authorization': f'Bearer {access_token}'}
    userinfo_response = requests.get(userinfo_url, headers=headers)
    userinfo_data = userinfo_response.json()

    # Extract the relevant user information
    google_id = userinfo_data['id']
    username = userinfo_data['email']
    name = userinfo_data['name']

    # Check if the user already exists in the database
    user = get_user_by_username(username)
    if user:
        # User already exists, log them in
        session['username'] = user['username']
        return redirect(url_for('welcome'))
    else:
        # User doesn't exist, register them
        user = register_google_user(google_id, username, name)
        if user:
            session['username'] = user['username']
            return redirect(url_for('welcome'))
        else:
            return 'Failed to register user'

@app.route('/login/facebook')
def facebook_login():
    # Generate the Facebook OAuth authorization URL
    facebook_auth_url = f'https://www.facebook.com/v13.0/dialog/oauth?client_id={FACEBOOK_APP_ID}&redirect_uri={url_for("facebook_callback", _external=True)}&scope=email&auth_type=rerequest&display=popup'
    
    # Redirect the user to the Facebook OAuth authorization page
    return redirect(facebook_auth_url)

@app.route('/login/facebook/callback')
def facebook_callback():
    # Retrieve the authorization code from the request
    code = request.args.get('code')

    # Exchange the authorization code for an access token
    token_url = f'https://graph.facebook.com/v13.0/oauth/access_token?client_id={FACEBOOK_APP_ID}&client_secret={FACEBOOK_APP_SECRET}&redirect_uri={url_for("facebook_callback", _external=True)}&code={code}'
    token_response = requests.get(token_url)
    token_data = token_response.json()
    access_token = token_data['access_token']

    # Retrieve the user's information using the access token
    userinfo_url = f'https://graph.facebook.com/me?fields=id,name,email&access_token={access_token}'
    userinfo_response = requests.get(userinfo_url)
    userinfo_data = userinfo_response.json()

    # Extract the relevant user information
    facebook_id = userinfo_data['id']
    username = userinfo_data['email']
    name = userinfo_data['name']

    # Check if the user already exists in the database
    user = get_user_by_username(username)
    if user:
        # User already exists, log them in
        session['username'] = user['username']
        return redirect(url_for('welcome'))
    else:
        # User doesn't exist, register them
        user = register_facebook_user(facebook_id, username, name)
        if user:
            session['username'] = user['username']
            return redirect(url_for('welcome'))
        else:
            return 'Failed to register user'

if __name__ == '__main__':
    conn = create_connection()
    create_tables(conn)
    app.run(debug=True)