import os
from flask import Flask, render_template, request, redirect
from pymongo import MongoClient

app = Flask(__name__)

# 1. MONGODB CONNECTION
# Use an environment variable in production, with a local fallback for development.
MONGO_URI = os.environ.get("MONGO_URI")
if not MONGO_URI:
    MONGO_URI = "mongodb+srv://portfolio-admin:YOUR_PASSWORD@cluster0.43cmhyo.mongodb.net/?appName=Cluster0"

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

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)