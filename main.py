import os
import sqlite3
from flask import Flask, render_template, request, jsonify
import majal # استدعاء محرك لغتك majal.py

app = Flask(__name__)

# ==========================================
# إعداد قاعدة البيانات (المخزن)
# ==========================================
def init_db():
    # إنشاء ملف قاعدة البيانات إذا لم يكن موجوداً
    conn = sqlite3.connect('majal_store.db')
    cursor = conn.cursor()
    # إنشاء جدول للمنتجات: الاسم، السعر، والتصنيف
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            category TEXT
        )
    ''')
    conn.commit()
    conn.close()

# ==========================================
# المسارات (Routes)
# ==========================================

@app.route('/')
def index():
    # فتح واجهة المستخدم
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run_code():
    user_code = request.json.get('code', '')
    
    # التأكد من جاهزية قاعدة البيانات في كل مرة
    init_db()
    
    try:
        # 1. تحليل الكود عبر محرك مجال (Tokenizer)
        tokens = majal.tokenize(user_code)
        
        # 2. تجهيز رسالة النتيجة للمستخدم
        # حالياً نعيد له الرموز التي تم تحليلها بنجاح
        result = "✅ تم الاتصال بمحرك مجال 2.0\n"
        result += "---------------------------\n"
        result += "الرموز المكتشفة:\n"
        for tok in tokens:
            result += f"<- {tok[0]}: {tok[1]} ->\n"
        
        result += "\n[نظام التخزين]: قاعدة بيانات المتاجر جاهزة للربط."
        
        return jsonify({'result': result})
        
    except Exception as e:
        # في حال وجود خطأ برمج في كود المستخدم
        return jsonify({'result': f"❌ خطأ في محرك مجال: {str(e)}"})

# ==========================================
# تشغيل السيرفر
# ==========================================
if __name__ == '__main__':
    # إعدادات التشغيل المتوافقة مع سيرفرات Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
