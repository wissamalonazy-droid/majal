from flask import Flask, request, jsonify, render_template
import majal
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    data = request.get_json()
    code = data.get('code', '')
    # استدعاء دالة التشغيل من نواة مجال
    output = majal.run_interpreter(code)
    return jsonify({'result': output})

if __name__ == '__main__':
    # تشغيل السيرفر على البورت المخصص لـ Render
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    
