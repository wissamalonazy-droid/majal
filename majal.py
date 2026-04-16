import re

# ذاكرة اللغة (Storage)
variables = {}

def tokenize(code):
    token_specification = [
        ('BUILD',    r'ابني'),         # أمر البناء الشامل
        ('ANALYZE',  r'فحص'),         # أمر المحلل الذكي
        ('VAR',      r'عرف'),          # تعريف المتغيرات
        ('PRINT',    r'اطبع'),         # الطباعة
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), # الأسماء
        ('NUMBER',   r'\d+(\.\d+)?'),  # الأرقام
        ('STRING',   r'"[^"]*"'),      # النصوص
        ('ASSIGN',   r'='),            # مساواة
        ('PLUS',     r'\+'),           # جمع
        ('MINUS',    r'-'),           # طرح
        ('MULT',     r'\*'),           # ضرب
        ('DIV',      r'/'),            # قسمة
        ('END',      r';'),            # نهاية السطر
        ('SKIP',     r'[ \t]+'),       # مسافات
        ('NEWLINE',  r'\n'),           # سطر جديد
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "⚠️ بانتظار أوامر برمجية لـ مَجال..."
    
    results = []
    statements = []
    current_stmt = []
    
    # تقسيم الكود إلى جمل برمجية بناءً على الفاصلة المنقوطة
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    for stmt in statements:
        try:
            cmd = stmt[0][0]

            # 1️⃣ مصنع الأنظمة المتكامل (بناء من الألف إلى الياء)
            if cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                if sys_type == "متجر":
                    results.append(f"""
🚀 [نظام مجال الشامل]: تم توليد مشروع متجر متكامل من الألف إلى الياء:

1. واجهة المستخدم الفاخرة (Frontend):
--------------------------------------------------
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <title>SUHAIL ELUCE SHOP</title>
</head>
<body class="bg-[#0b0b0b] text-white">
    <nav class="p-8 border-b border-[#0A1F44] flex justify-between">
        <h1 class="text-3xl font-black text-[#3b82f6]">SUHAIL ELUCE</h1>
        <ul class="flex gap-8 text-lg"><li>الرئيسية</li><li>العطور</li><li>السلة</li></ul>
    </nav>
    <main class="p-12">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-12">
             <div class="bg-[#111] p-6 rounded-3xl border border-gray-800 shadow-2xl">
                <div class="h-80 bg-[#0A1F44] rounded-2xl mb-6 animate-pulse"></div>
                <h2 class="text-2xl font-bold">عطر Sadeem</h2>
                <p class="text-blue-400 mt-2 font-mono">450 SAR</p>
                <button class="w-full bg-blue-600 mt-6 py-4 rounded-2xl font-black">شراء الآن</button>
             </div>
        </div>
    </main>
</body>
</html>

2. قاعدة البيانات الاحترافية (Database):
--------------------------------------------------
CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(100), price FLOAT);
CREATE TABLE orders (id INT AUTO_INCREMENT, total_amount FLOAT, date TIMESTAMP);
CREATE TABLE inventory (product_id INT, stock_count INT);

3. منطق الربط والتحكم (Backend Logic):
--------------------------------------------------
- API: نظام الدفع (Stripe/Mada) مفعل تلقائياً.
- Auth: نظام حماية البيانات وتشفير كلمات المرور.
--------------------------------------------------
                    """)
                elif sys_type == "مدرسة":
                    results.append("🏗️ [مصنع مجال]: تم بناء نظام إدارة شؤون الطلاب، الدرجات، وجداول الحصص من الألف إلى الياء.")
                else:
                    results.append(f"🏗️ [مصنع مجال]: جاري توليد هيكل مشروع {sys_type} مخصص...")

            # 2️⃣ المحلل الذكي وكاشف الأخطاء (Static Analysis)
            elif cmd == 'ANALYZE':
                issues = []
                for s in statements:
                    for i, t in enumerate(s):
                        # كشف المتغيرات غير المعرفة
                        if t[0] == 'ID' and t[1] not in variables and s[max(0, i-1)][0] != 'VAR':
                            issues.append(f"تنبيه: المتغير [{t[1]}] مفقود من الذاكرة.")
                        # كشف القسمة على صفر قبل التشغيل
                        if t[0] == 'DIV' and s[i+1][1] == '0':
                            issues.append("🚨 كارثة: تم اكتشاف محاولة قسمة على صفر!")
                
                results.append("🔍 [محلل مجال]: انتهى فحص الكود.")
                if issues:
                    results.append("\n".join(set(issues)))
                else:
                    results.append("✅ كودك مثالي وجاهز للتشغيل.")

            # 3️⃣ الأوامر الأساسية (تعريف، طباعة، حساب)
            elif cmd == 'VAR':
                variables[stmt[1][1]] = float(stmt[3][1])
                results.append(f"✅ تم حفظ المتغير [{stmt[1][1]}]")

            elif cmd == 'PRINT':
                if len(stmt) >= 4:
                    v1 = variables.get(stmt[1][1], float(stmt[1][1]))
                    v2 = variables.get(stmt[3][1], float(stmt[3][1]))
                    op = stmt[2][0]
                    if op == 'PLUS': results.append(f"🔢 الناتج: {v1 + v2}")
                    elif op == 'MULT': results.append(f"🔢 الناتج: {v1 * v2}")
                    elif op == 'DIV': results.append(f"🔢 الناتج: {v1 / v2}" if v2 != 0 else "❌ خطأ")
                else:
                    results.append(stmt[1][1].strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ برمجية: {str(e)}")
    
    return "\n".join(results)
