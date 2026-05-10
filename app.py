from flask import Flask, redirect, url_for, session, jsonify
from authlib.integrations.flask_client import OAuth
from datetime import datetime

# Initialize App
app = Flask(__name__)
app.secret_key = "SECRET_KEY"
oauth = OAuth(app)

# Configure GitHub OAuth
github = oauth.register(
    name='github',
    client_id='Ov23limqt1g76ytQtapG',         
    client_secret='67c3d1dae0dca73aba526e212c4f8a873573f2dd', 
    access_token_url='https://github.com/login/oauth/access_token',
    authorize_url='https://github.com/login/oauth/authorize',
    api_base_url='https://api.github.com/',
    client_kwargs={'scope': 'user:email'},
)

css_style = """
<style>
    :root {
        --ios-bg: #f2f2f7;
        --ios-card: #ffffff;
        --ios-text: #000000;
        --ios-subtext: #8e8e93;
        --ios-separator: rgba(60, 60, 67, 0.29);
        --ios-blue: #007aff;
        --ios-red: #ff3b30;
    }
    body { 
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "Helvetica Neue", sans-serif; 
        background-color: var(--ios-bg); 
        display: flex; justify-content: center; align-items: center; 
        min-height: 100vh; margin: 0; color: var(--ios-text);
        -webkit-font-smoothing: antialiased;
    }
    .iphone-container { width: 100%; max-width: 390px; padding: 20px; box-sizing: border-box; }
    
    .profile-header { text-align: center; margin-bottom: 24px; }
    .avatar { width: 100px; height: 100px; border-radius: 50%; margin-bottom: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
    h1 { font-size: 28px; font-weight: 700; margin: 0; letter-spacing: -0.5px; }
    .handle { color: var(--ios-subtext); font-size: 15px; margin-top: 4px; }
    .bio { font-size: 15px; margin: 12px 0; line-height: 1.4; padding: 0 10px; }
    
    .ios-list { background: var(--ios-card); border-radius: 10px; overflow: hidden; margin-bottom: 20px; }
    .ios-list-item { display: flex; justify-content: space-between; padding: 12px 16px; border-bottom: 0.5px solid var(--ios-separator); font-size: 16px; }
    .ios-list-item:last-child { border-bottom: none; }
    .label { color: var(--ios-text); }
    .value { color: var(--ios-subtext); text-align: right; max-width: 60%; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    
    .stats-row { display: flex; justify-content: space-evenly; background: var(--ios-card); border-radius: 10px; padding: 16px 0; margin-bottom: 20px; text-align: center; }
    .stat-val { display: block; font-size: 17px; font-weight: 600; }
    .stat-label { font-size: 12px; color: var(--ios-subtext); margin-top: 4px; }
    
    .btn { display: block; width: 100%; padding: 14px; border-radius: 14px; text-decoration: none; font-size: 17px; font-weight: 600; text-align: center; margin-bottom: 12px; box-sizing: border-box; cursor: pointer; border: none; }
    .btn-primary { background: #000000; color: #ffffff; }
    .btn-secondary { background: var(--ios-card); color: var(--ios-blue); }
    .btn-danger { background: var(--ios-card); color: var(--ios-red); }
</style>
"""

# 1. VISUAL LOGIN PAGE
@app.route('/login')
def login():
    return f'''
    {css_style}
    <div class="iphone-container" style="text-align: center;">
        <h1 style="margin-bottom: 8px;">OAuth Lab</h1>
        <p style="color: #8e8e93; margin-bottom: 32px;">System Integration & Architecture</p>
        <a href="/authorize" class="btn btn-primary">Sign in with GitHub</a>
    </div>
    '''

@app.route('/authorize')
def authorize():
    return github.authorize_redirect(url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = github.authorize_access_token()
    resp = github.get('user') 
    user = resp.json()
    session['user'] = user
    return redirect('/profile')

# 3. SUCCESSFUL LOGIN & 4. UNAUTHORIZED ACCESS
@app.route('/profile')
def profile():
    if 'user' not in session:
        return f'''
        {css_style}
        <div class="iphone-container" style="text-align: center;">
            <h1 style="color: #ff3b30; margin-bottom: 8px;">Unauthorized</h1>
            <p style="color: #8e8e93; margin-bottom: 32px;">Authentication required to view profile.</p>
            <a href="/login" class="btn btn-primary">Return to Sign In</a>
        </div>
        ''', 401
    
    user = session['user']
    
    avatar = user.get('avatar_url', '')
    name = user.get('name') or "GitHub User"
    login_handle = user.get('login', '')
    bio = user.get('bio') or "No bio available."
    
    created_at = user.get('created_at', '')
    if created_at:
        try:
            date_obj = datetime.strptime(created_at, "%Y-%m-%dT%H:%M:%SZ")
            created_at = date_obj.strftime("%b %Y")
        except:
            pass

    return f'''
    {css_style}
    <div class="iphone-container">
        
        <div class="profile-header">
            <img src="{avatar}" class="avatar" alt="Avatar">
            <h1>{name}</h1>
            <div class="handle">@{login_handle}</div>
            <div class="bio">{bio}</div>
        </div>

        <div class="stats-row">
            <div><span class="stat-val">{user.get('public_repos', 0)}</span><span class="stat-label">Repos</span></div>
            <div><span class="stat-val">{user.get('followers', 0)}</span><span class="stat-label">Followers</span></div>
            <div><span class="stat-val">{user.get('following', 0)}</span><span class="stat-label">Following</span></div>
        </div>

        <div class="ios-list">
            <div class="ios-list-item"><span class="label">Email</span> <span class="value">{user.get('email') or 'Hidden'}</span></div>
            <div class="ios-list-item"><span class="label">Company</span> <span class="value">{user.get('company') or 'None'}</span></div>
            <div class="ios-list-item"><span class="label">Location</span> <span class="value">{user.get('location') or 'None'}</span></div>
            <div class="ios-list-item"><span class="label">Joined</span> <span class="value">{created_at or 'Unknown'}</span></div>
        </div>

        <a href="{user.get('html_url', '#')}" target="_blank" class="btn btn-secondary">View on GitHub</a>
        <a href="/logout" class="btn btn-danger">Log Out</a>
        
    </div>
    '''

# BONUS CHALLENGE: Protected route
@app.route('/api/secure-data')
def secure_data():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized Access", "status": 401}), 401
    return jsonify({"message": "This is highly secure data!", "status": "success"})

# 5. LOGOUT RESULT
@app.route('/logout')
def logout():
    session.pop('user', None)
    return f'''
    {css_style}
    <div class="iphone-container" style="text-align: center;">
        <h1 style="color: #000000; margin-bottom: 8px;">Signed Out</h1>
        <p style="color: #8e8e93; margin-bottom: 32px;">Your session has been ended.</p>
        <a href="/profile" class="btn btn-secondary">Verify Sign Out</a>
    </div>
    '''

if __name__ == '__main__':
    app.run(debug=True)