from flask import Flask, request, jsonify, render_template
import re

app = Flask(__name__)

def run_interpreter(raw_code):
    # 1. إذا كان الكود واجهة رسومية (HTML)
    if any(tag in raw_code.lower() for tag in ["<!doctype html>", "<html", "<body"]):
        # ذكاء النواة: حقن وسم الـ Viewport لضمان عمل المحاكي بدقة الجوال
        if "<head>" in raw_code.lower():
            responsive_meta = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
            raw_code = raw_code.replace("<head>", f"<head>\n    {responsive_meta}")
        return raw_code

    # 2. إذا كان الكود منطق برمجى (عرف / اطبع)
    env = {'vars': {}}
    results = []
    lines = raw_code.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("//"): continue
        try:
            if "عرف" in line and "=" in line:
                clean_line = line.replace("عرف", "").replace(";", "").strip()
                parts = clean_line.split("=")
                var_name = parts[0].strip()
                expression = parts[1].strip()
                for v_name, v_val in env['vars'].items():
                    expression = expression.replace(v_name, str(v_val))
                env['vars'][var_name] = eval(expression)
                results.append(f"💠 تم حفظ {var_name}")
            elif "اطبع" in line:
                content = line.replace("اطبع", "").replace(";", "").strip()
                val = env['vars'].get(content, content.strip('"'))
                results.append(f"📟 {val}")
        except:
            results.append(f"⚠️ خطأ في: {line}")
            
    return "\n".join(results) if results else "📝 اكتب كودك..."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run', methods=['POST'])
def run():
    code = request.json.get('code', '')
    result = run_interpreter(code)
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)
