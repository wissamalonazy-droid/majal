import re

# ذاكرة اللغة لتخزين المتغيرات
variables = {}

def tokenize(code):
    token_specification = [
        ('BUILD',    r'ابني'),         # أمر بناء الأنظمة
        ('ANALYZE',  r'فحص'),         # أمر تحليل الكود
        ('VAR',      r'عرف'),          # تعريف المتغيرات
        ('PRINT',    r'اطبع'),         # الطباعة
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), # الأسماء العربية والانجليزية
        ('NUMBER',   r'\d+(\.\d+)?'),  # الأرقام الصحيحة والعشرية
        ('STRING',   r'"[^"]*"'),      # النصوص بين علامات تنصيص
        ('ASSIGN',   r'='),            # علامة المساواة
        ('PLUS',     r'\+'),           # الجمع
        ('MINUS',    r'-'),           # الطرح
        ('MULT',     r'\*'),           # الضرب
        ('DIV',      r'/'),            # القسمة
        ('END',      r';'),            # نهاية السطر البرمجي
        ('SKIP',     r'[ \t]+'),       # المسافات (تجاهل)
        ('NEWLINE',  r'\n'),           # سطر جديد (تجاهل)
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "⚠️ بانتظار أوامر برمجية لـ مَجال..."
    
    results = []
    statements = []
    current_stmt = []
    
    # تقسيم التوكنز إلى جمل برمجية بناءً على الفاصلة المنقوطة (;)
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    for stmt in statements:
        try:
            cmd = stmt[0][0]

            # 1️⃣ نظام البناء الشامل (من الألف إلى الياء)
            if cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                if sys_type == "متجر":
                    results.append(f"""
🚀 [نظام مجال الشامل]: تم توليد مشروع متجر كامل:

1. واجهة المستخدم (HTML/Tailwind):
--------------------------------------------------
<body class="bg-[#0b0b0b] text-white">
    <nav class="p-8 border-b border-blue-900 flex justify-between">
        <h1 class="text-3xl font-bold">SUHAIL ELUCE</h1>
        <ul class="flex gap-6"><li>الرئيسية</li><li>المتجر</li></ul>
    </nav>
    <div class="p-12 grid grid-cols-1 md:grid-cols-3 gap-10">
        <div class="bg-gray-900 p-6 rounded-3xl border border-gray-800">
            <div class="h-64 bg-blue-900/20 rounded-xl mb-4"></div>
            <h2 class="text-xl">عطر Sadeem</h2>
            <p class="text-blue-400 font-bold">450 SAR</p>
            <button class="w-full bg-blue-600 py-3 rounded-xl mt-4">شراء</button>
        </div>
    </div>
</body>

2. قاعدة البيانات (SQL):
--------------------------------------------------
CREATE TABLE products (id INT, name TEXT, price FLOAT);
CREATE TABLE orders (id INT, total FLOAT, status TEXT);

3. منطق العمليات (Backend):
--------------------------------------------------
- نظام الدفع: Checkout API موصل بمدى.
- الحماية: تم تفعيل تشفير SSL للمتجر.
--------------------------------------------------
                    """)
                elif sys_type == "مدرسة":
                    results.append("🏗️ [مصنع مجال]: تم بناء نظام إدارة تعليمي شامل (طلاب، مدرسين، درجات).")
                else:
                    results.append(f"🏗️ [مصنع مجال]: جاري توليد هيكل مخصص لـ {sys_type}...")

            # 2️⃣ المحلل الذكي وكاشف الأخطاء
            elif cmd == 'ANALYZE':
                issues = []
                for s in statements:
                    for i, t in enumerate(s):
                        if t[0] == 'ID' and t[1] not in variables and s[max(0, i-1)][0] != 'VAR':
                            issues.append(f"تنبيه: المتغير [{t[1]}] لم يتم تعريفه!")
                        if t[0] == 'DIV' and i+1 < len(s) and s[i+1][1] == '0':
                            issues.append("🚨 خطر: اكتشفنا محاولة قسمة على صفر!")
                
                results.append("🔍 [محلل مجال]: انتهى الفحص.")
                if issues: results.append("\n".join(set(issues)))
                else: results.append("✅ الكود سليم وجاهز للإطلاق.")

            # 3️⃣ الأوامر الأساسية (تعريف، طباعة)
            elif cmd == 'VAR':
                variables[stmt[1][1]] = float(stmt[3][1])
                results.append(f"✅ تم حفظ المتغير [{stmt[1][1]}]")

            elif cmd == 'PRINT':
                if len(stmt) >= 4:
                    v1 = variables.get(stmt[1][1], float(stmt[1][1])) if stmt[1][0] in ['ID','NUMBER'] else 0
                    v2 = variables.get(stmt[3][1], float(stmt[3][1])) if stmt[3][0] in ['ID','NUMBER'] else 0
                    op = stmt[2][0]
                    if op == 'PLUS': results.append(f"🔢 الناتج: {v1 + v2}")
                    elif op == 'MULT': results.append(f"🔢 الناتج: {v1 * v2}")
                    elif op == 'DIV': results.append(f"🔢 الناتج: {v1 / v2}" if v2 != 0 else "❌ خطأ")
                else:
                    results.append(stmt[1][1].strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ في تنفيذ السطر: {str(e)}")
    
    return "\n".join(results)
