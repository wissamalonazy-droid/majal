import re

# ذاكرة اللغة لتخزين المتغيرات (Storage)
variables = {}

def tokenize(code):
    token_specification = [
        ('BUILD',    r'ابني'),         
        ('ANALYZE',  r'فحص'),         
        ('VAR',      r'عرف'),          
        ('PRINT',    r'اطبع'),         
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'),  
        ('STRING',   r'"[^"]*"'),      
        ('ASSIGN',   r'='),            
        ('PLUS',     r'\+'),           
        ('MINUS',    r'-'),           
        ('MULT',     r'\*'),           
        ('DIV',      r'/'),            
        ('END',      r';'),            
        ('SKIP',     r'[ \t]+'),       
        ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "⚠️ بانتظار أوامر برمجية لـ مَجال..."
    
    results = []
    statements = []
    current_stmt = []
    
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    for stmt in statements:
        try:
            cmd = stmt[0][0]

            # 1️⃣ نظام البناء الديناميكي (بناء أي متجر يطلبه المبرمج)
            if cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                
                # جلب اسم المتجر من الذاكرة (إذا عرفه المبرمج) أو استخدام اسم افتراضي
                raw_name = variables.get("اسم_المتجر", "SUHAIL ELUCE")
                store_name = str(raw_name).strip('"')

                if sys_type == "متجر":
                    results.append(f"""
🚀 [نظام مجال الشامل]: تم توليد مشروع متكامل لـ ({store_name}) من الألف إلى الياء:

1. واجهة المستخدم (HTML/Tailwind):
--------------------------------------------------
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <title>{store_name}</title>
</head>
<body class="bg-[#0b0b0b] text-white">
    <nav class="p-8 border-b border-blue-900 flex justify-between items-center">
        <h1 class="text-3xl font-black text-blue-500 uppercase">{store_name}</h1>
        <ul class="flex gap-8 text-lg font-bold">
            <li class="hover:text-blue-400 cursor-pointer">الرئيسية</li>
            <li class="hover:text-blue-400 cursor-pointer">منتجاتنا</li>
            <li class="bg-blue-600 px-4 py-1 rounded-lg">السلة</li>
        </ul>
    </nav>
    <main class="p-12 text-center">
        <h2 class="text-5xl font-extrabold mb-10">مرحباً بكم في {store_name}</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
             <div class="bg-gray-900 p-8 rounded-[40px] border border-gray-800 shadow-2xl transition-transform hover:scale-105">
                <div class="h-64 bg-gradient-to-br from-blue-900 to-black rounded-3xl mb-6"></div>
                <h3 class="text-2xl font-bold">المنتج الأول</h3>
                <p class="text-blue-400 mt-2 font-mono text-xl">السعر حسب الطلب</p>
                <button class="w-full bg-blue-600 mt-8 py-4 rounded-2xl font-black tracking-widest uppercase hover:bg-blue-500">أضف للسلة</button>
             </div>
        </div>
    </main>
</body>
</html>

2. قاعدة البيانات المنظمة (SQL):
--------------------------------------------------
CREATE TABLE {store_name.replace(' ', '_')}_products (id INT, name VARCHAR(100), price FLOAT);
CREATE TABLE {store_name.replace(' ', '_')}_orders (id INT, total_amount FLOAT, date TIMESTAMP);

3. ملف الإعدادات (JSON):
--------------------------------------------------
{{
    "project_name": "{store_name}",
    "owner": "Wesam",
    "currency": "SAR",
    "status": "Ready for Deployment"
}}
--------------------------------------------------
                    """)
                elif sys_type == "مدرسة":
                    results.append(f"🏗️ [مصنع مجال]: تم بناء نظام إدارة تعليمي كامل لـ ({store_name}).")
                else:
                    results.append(f"🏗️ [مصنع مجال]: جاري بناء نظام {sys_type} مخصص...")

            # 2️⃣ المحلل الذكي
            elif cmd == 'ANALYZE':
                issues = []
                for s in statements:
                    for i, t in enumerate(s):
                        if t[0] == 'ID' and t[1] not in variables and s[max(0, i-1)][0] != 'VAR':
                            issues.append(f"تنبيه: المتغير [{t[1]}] مفقود من الذاكرة.")
                        if t[0] == 'DIV' and i+1 < len(s) and s[i+1][1] == '0':
                            issues.append("🚨 خطر: اكتشفنا محاولة قسمة على صفر!")
                
                results.append("🔍 [محلل مجال]: انتهى الفحص.")
                if issues: results.append("\n".join(set(issues)))
                else: results.append("✅ الكود سليم واحترافي.")

            # 3️⃣ تعريف المتغيرات (دعم النصوص والأرقام)
            elif cmd == 'VAR':
                var_name = stmt[1][1]
                var_value = stmt[3][1]
                # تخزين القيمة (سواء كانت نصاً أو رقماً)
                variables[var_name] = var_value
                results.append(f"✅ تم حفظ [{var_name}] في الذاكرة.")

            elif cmd == 'PRINT':
                target = stmt[1][1]
                if target in variables:
                    results.append(str(variables[target]).strip('"'))
                else:
                    results.append(target.strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ: {str(e)}")
    
    return "\n".join(results)
