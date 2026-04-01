from flask import Flask, request, render_template, send_file, jsonify
import sqlite3
import os
import fileinput
import tempfile
from datetime import datetime
import shutil

app = Flask(__name__)
DB_FILE = 'stats.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    # Table for conversions
    c.execute('''CREATE TABLE IF NOT EXISTS conversions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, ip_address TEXT, count INTEGER)''')
    # Table for visits
    c.execute('''CREATE TABLE IF NOT EXISTS visits
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, ip_address TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.before_request
def log_visit():
    if request.endpoint == 'index':
        ip = request.remote_addr
        date = datetime.now().strftime('%Y-%m-%d')
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        # count unique IP per day
        c.execute("SELECT id FROM visits WHERE date=? AND ip_address=?", (date, ip))
        if not c.fetchone():
            c.execute("INSERT INTO visits (date, ip_address) VALUES (?, ?)", (date, ip))
        conn.commit()
        conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    if 'files' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('files')
    if not files or files[0].filename == '':
        return jsonify({'error': 'No files selected'}), 400

    ip = request.remote_addr
    date = datetime.now().strftime('%Y-%m-%d')

    # Create a temp directory
    temp_dir = tempfile.mkdtemp()
    
    file_count = 0
    try:
        for file in files:
            if file.filename:
                file_count += 1
                filepath = os.path.join(temp_dir, file.filename)
                file.save(filepath)
                
                # Convert logic
                with fileinput.input(filepath, inplace=True, encoding='utf-8', errors='ignore') as f:
                    for line in f:
                        if f.isfirstline():
                            print('HDR              55MFT                               096N', end='\n')
                        else:
                            print(line, end='')

        # Log conversion
        if file_count > 0:
            conn = sqlite3.connect(DB_FILE)
            c = conn.cursor()
            c.execute("INSERT INTO conversions (date, ip_address, count) VALUES (?, ?, ?)", (date, ip, file_count))
            conn.commit()
            conn.close()

        # Zip it up
        zip_path = os.path.join(tempfile.gettempdir(), f"converted_{datetime.now().strftime('%Y%m%d%H%M%S')}")
        shutil.make_archive(zip_path, 'zip', temp_dir)
        zip_filename = f"{zip_path}.zip"
        
        return send_file(zip_filename, as_attachment=True, download_name='converted_files.zip')
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

@app.route('/stats')
def stats():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    # conversions by date
    c.execute("SELECT date, SUM(count) as total FROM conversions GROUP BY date ORDER BY date DESC")
    conversions_by_date = c.fetchall()
    
    # visitors by date
    c.execute("SELECT date, COUNT(ip_address) as unique_visits FROM visits GROUP BY date ORDER BY date DESC")
    visitors_by_date = c.fetchall()
    
    conn.close()
    
    return render_template('stats.html', conversions=conversions_by_date, visitors=visitors_by_date)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
