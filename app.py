from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# 1. SMART DATABASE PATH (Render uses /tmp/ for temporary storage)
if os.environ.get('RENDER'):
    DB_PATH = '/tmp/database.db'
else:
    DB_PATH = 'database.db'

# 2. DATABASE INITIALIZATION
def init_db():
    conn = sqlite3.connect(DB_PATH)
    conn.execute('CREATE TABLE IF NOT EXISTS messages (name TEXT, email TEXT, message TEXT)')
    conn.close()

# 3. AUTOMATIC TABLE CREATION
init_db()

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

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute("INSERT INTO messages (name, email, message) VALUES (?, ?, ?)", (name, email, msg))
            conn.commit()
            conn.close()
            # Glassmorphism Success Message
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

# 4. FUTURISTIC GLASSMORPHISM DATA VIEWER
@app.route('/view_data')
def view_data():
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM messages")
        rows = cursor.fetchall()
        conn.close()
        
        style = """
        <style>
            body { 
                background: url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?ixlib=rb-1.2.1&auto=format&fit=crop&w=1352&q=80');
                background-size: cover;
                background-attachment: fixed;
                color: white; 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                padding: 40px;
                display: flex;
                flex-direction: column;
                align-items: center;
            }
            .container {
                background: rgba(255, 255, 255, 0.05);
                backdrop-filter: blur(15px);
                -webkit-backdrop-filter: blur(15px);
                border-radius: 20px;
                border: 1px solid rgba(255, 255, 255, 0.18);
                padding: 30px;
                width: 90%;
                max-width: 1000px;
                box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.5);
            }
            h1 { 
                text-align: center; 
                letter-spacing: 4px; 
                text-transform: uppercase;
                color: #00d2ff;
                text-shadow: 0 0 10px #00d2ff;
            }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th { padding: 15px; text-align: left; color: #00d2ff; border-bottom: 2px solid rgba(0, 210, 255, 0.3); }
            td { padding: 15px; border-bottom: 1px solid rgba(255, 255, 255, 0.1); }
            tr:hover { background: rgba(255, 255, 255, 0.05); }
            .back-btn { 
                display: inline-block; 
                margin-top: 30px; 
                padding: 12px 25px; 
                background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%);
                color: white; 
                text-decoration: none; 
                border-radius: 50px;
                font-weight: bold;
                transition: 0.3s;
            }
            .back-btn:hover { transform: scale(1.05); box-shadow: 0 0 15px #00d2ff; }
        </style>
        """
        
        html = style + '<div class="container">'
        html += "<h1>🛰️ DATA_LOG_COLLECTOR</h1><table><tr><th>NAME</th><th>IDENTITY_EMAIL</th><th>TRANSMISSION</th></tr>"
        for row in rows:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td></tr>"
        html += "</table><center><a href='/' class='back-btn'>RETURN TO HUB</a></center></div>"
        
        return html
    except Exception as e:
        return f"<h1>STORAGE_ACCESS_DENIED: {e}</h1>"

# UPDATED: Setup for Cloud and Local Execution
if __name__ == '__main__':
    # Initialize the DB if it doesn't exist
    init_db()
    
    # Get port from environment (Render sets this) or default to 5000
    port = int(os.environ.get("PORT", 5000))
    
    # Run the app
    # host='0.0.0.0' is required for cloud services to access the app
    app.run(host='0.0.0.0', port=port)