import os
from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # dotenv not installed, skip loading .env


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")

# 1. MONGODB CONNECTION
# Use an environment variable in production, with a local fallback for development.
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    MONGO_URI = "mongodb+srv://portfolio-admin:YOUR_ACTUAL_PASSWORD@cluster0.43cmhyo.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
messages_col = None
try:
    client.admin.command("ping")
    db = client.portfolio_website
    messages_col = db.messages
except Exception as e:
    print(f"MongoDB connection warning: {e}")
    # continue running the app even if MongoDB is unavailable

portfolio_data = {
    'student_name': 'Abhishek P',
    'introduction_para_1': "Merging data analytics with modern web development to build high-performance digital experiences."
}

@app.route('/')
def index():
    return render_template('index.html', data=portfolio_data)

@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        msg = request.form.get('message')

        if messages_col is None:
            return "<body style='background:#000; color:#ff6b6b; padding:50px;'><h1>DATABASE_NOT_AVAILABLE</h1><p>The app can run, but MongoDB is not configured or reachable.</p></body>"

        try:
            # MongoDB Insertion
            messages_col.insert_one({
                "name": name,
                "email": email,
                "message": msg
            })
            
            return """
            <body style="background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 50px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2); text-align: center; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);">
                    <h1 style="color: #00d2ff;">DATA SECURED</h1>
                    <p>Information has been successfully uploaded to the cloud matrix.</p>
                    <a href='/' style="color: #00d2ff; text-decoration: none; font-weight: bold;">[ RETURN TO INTERFACE ]</a>
                </div>
            </body>
            """
        except Exception as e:
            return f"<body style='background:#000; color:red; padding:50px;'><h1>SYSTEM_ERROR: {e}</h1></body>"

@app.route('/view_data')
def view_data():
    if messages_col is None:
        return "<body style='background:#000; color:#ff6b6b; padding:50px;'><h1>DATABASE_NOT_AVAILABLE</h1><p>The app can run, but MongoDB is not configured or reachable.</p></body>"

    try:
        # Retrieve all messages from MongoDB
        rows = list(messages_col.find())
        
        style = """
        <style>
            body { 
                background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80');
                background-size: cover; background-attachment: fixed; color: white; 
                font-family: 'Segoe UI', sans-serif; padding: 40px; display: flex; flex-direction: column; align-items: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.18); padding: 30px; width: 90%; max-width: 1000px;
            }
            h1 { text-align: center; letter-spacing: 4px; color: #00d2ff; text-shadow: 0 0 10px #00d2ff; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th { padding: 15px; text-align: left; color: #00d2ff; border-bottom: 2px solid rgba(0, 210, 255, 0.3); }
            td { padding: 15px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
            .back-btn { 
                display: inline-block; margin-top: 30px; padding: 12px 25px; 
                background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
                color: white; text-decoration: none; border-radius: 50px; font-weight: bold;
            }
        </style>
        """
        
        html = style + '<div class="container">'
        html += "<h1>🛰️ DATA_LOG_COLLECTOR</h1><table><tr><th>NAME</th><th>IDENTITY_EMAIL</th><th>TRANSMISSION</th></tr>"
        for row in rows:
            html += f"<tr><td>{row.get('name')}</td><td>{row.get('email')}</td><td>{row.get('message')}</td></tr>"
        html += "</table><center><a href='/' class='back-btn'>RETURN TO HUB</a></center></div>"
        
        return html
    except Exception as e:
        return f"<h1>STORAGE_ACCESS_DENIED: {e}</h1>"

@app.route('/admin')
def admin():
    if 'logged_in' in session:
        return redirect('/admin/dashboard')
    return '''
    <html>
    <head><title>Admin Access Portal</title></head>
    <body style="background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; font-family: 'Segoe UI', sans-serif; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
        <div style="background: rgba(255, 255, 255, 0.1); backdrop-filter: blur(10px); padding: 50px; border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.2); text-align: center; box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);">
            <h1 style="color: #00d2ff; text-shadow: 0 0 10px #00d2ff;">ADMIN ACCESS PORTAL</h1>
            <p>Enter credentials to access the control matrix</p>
            <form method="POST" action="/admin/login">
                <input type="text" name="username" placeholder="USERNAME" required style="display: block; margin: 15px auto; padding: 15px; width: 250px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); border-radius: 10px; color: white; font-size: 16px;"><br>
                <input type="password" name="password" placeholder="PASSWORD" required style="display: block; margin: 15px auto; padding: 15px; width: 250px; background: rgba(255,255,255,0.1); border: 1px solid rgba(255,255,255,0.3); border-radius: 10px; color: white; font-size: 16px;"><br>
                <button type="submit" style="padding: 15px 30px; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; border: none; border-radius: 50px; font-weight: bold; font-size: 16px; cursor: pointer;">ACCESS SYSTEM</button>
            </form>
        </div>
    </body>
    </html>
    '''

@app.route('/admin/login', methods=['POST'])
def admin_login():
    username = request.form.get('username')
    password = request.form.get('password')
    # Simple auth - change these in production
    if username == 'Abhishek' and password == 'Abhishek@2007':
        session['logged_in'] = True
        return redirect('/admin/dashboard')
    return '<h1>Invalid credentials</h1><a href="/admin">Try again</a>'

@app.route('/admin/dashboard')
def admin_dashboard():
    if 'logged_in' not in session:
        return redirect('/admin')
    if messages_col is None:
        return "<body style='background:#000; color:#ff6b6b; padding:50px;'><h1>DATABASE_NOT_AVAILABLE</h1><p>Cannot access messages.</p><a href='/admin/logout' style='color:#00d2ff;'>Logout</a></body>"
    try:
        rows = list(messages_col.find())
        html = '''
        <html>
        <head><title>Admin Control Matrix</title></head>
        <body style="background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); color: white; font-family: 'Segoe UI', sans-serif; padding: 40px; display: flex; flex-direction: column; align-items: center;">
            <div style="background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(15px); border-radius: 20px; border: 1px solid rgba(255, 255, 255, 0.18); padding: 30px; width: 90%; max-width: 1200px;">
                <h1 style="text-align: center; letter-spacing: 4px; color: #00d2ff; text-shadow: 0 0 10px #00d2ff;">🛰️ ADMIN CONTROL MATRIX</h1>
                <p style="text-align: center; color: #ccc;">Monitor incoming transmissions from the contact interface</p>
                <table style="width: 100%; border-collapse: collapse; margin-top: 20px;">
                    <tr style="color: #00d2ff; border-bottom: 2px solid rgba(0, 210, 255, 0.3);">
                        <th style="padding: 15px; text-align: left;">NAME</th>
                        <th style="padding: 15px; text-align: left;">IDENTITY_EMAIL</th>
                        <th style="padding: 15px; text-align: left;">TRANSMISSION</th>
                    </tr>
        '''
        for row in rows:
            html += f"<tr style='border-bottom: 1px solid rgba(255, 255, 255, 0.1);'><td style='padding: 15px;'>{row.get('name')}</td><td style='padding: 15px;'>{row.get('email')}</td><td style='padding: 15px;'>{row.get('message')}</td></tr>"
        html += f'''
                </table>
                <center style="margin-top: 30px;">
                    <a href="/" style="display: inline-block; padding: 12px 25px; background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%); color: white; text-decoration: none; border-radius: 50px; font-weight: bold; margin-right: 10px;">RETURN TO INTERFACE</a>
                    <a href="/admin/logout" style="display: inline-block; padding: 12px 25px; background: rgba(255,255,255,0.1); color: #00d2ff; text-decoration: none; border-radius: 50px; font-weight: bold; border: 1px solid #00d2ff;">LOGOUT</a>
                </center>
            </div>
        </body>
        </html>
        '''
        return html
    except Exception as e:
        return f"<body style='background:#000; color:red; padding:50px;'><h1>SYSTEM_ERROR: {e}</h1><a href='/admin/logout' style='color:#00d2ff;'>Logout</a></body>"

@app.route('/admin/logout')
def admin_logout():
    session.pop('logged_in', None)
    return redirect('/admin')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)