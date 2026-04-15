import os
import sqlite3
from flask import Flask, render_template, request, jsonify
import majal

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('majal_store.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, price REAL)
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    user_code = request.json.get('code', '')
    init_db()
    try:
        # 1. تحليل الكود
        tokens = majal.tokenize(user_code)
        
        # 2. تنفيذ الكود (هذا السطر الجديد المهم)
        execution_result = majal.run_interpreter(tokens)
        
        return jsonify({'result': execution_result})
    except Exception as e:
        return jsonify({'result': f"❌ خطأ: {str(e)}"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
