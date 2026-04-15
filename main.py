import os
from flask import Flask, render_template, request, jsonify
import majal  # هذا ينادي ملف majal.py اللي فيه المحرك حقك

app = Flask(__name__)

@app.route('/')
def index():
    # هذا يفتح صفحة الواجهة اللي حطيناها في مجلد templates
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    # هنا نستقبل الكود اللي كتبه المستخدم في الموقع
    user_code = request.json.get('code', '')
    
    try:
        # ننادي دالة الـ tokenize من محرك لغتك
        tokens = majal.tokenize(user_code)
        
        # حالياً سنعيد التوكنز كـ نتيجة للتأكد أن المحرك شغال
        # إذا جهزت الـ Parser والـ Interpreter سنقوم بتشغيلهم هنا
        result = "✅ تم التحليل بنجاح:\n" + str(tokens)
        return jsonify({'result': result})
        
    except Exception as e:
        # إذا فيه خطأ في كود المستخدم يطلعه له في الموقع
        return jsonify({'result': f"❌ خطأ في محرك مجال: {str(e)}"})

if __name__ == '__main__':
    # Render يحتاج السيرفر يشتغل على بورت معين
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
