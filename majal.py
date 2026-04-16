import re

# ذاكرة اللغة لتخزين المتغيرات
variables = {}

def tokenize(code):
    token_specification = [
        ('IF',       r'إذا'),          
        ('BUILD',    r'ابني'),         
        ('VAR',      r'عرف'),          
        ('PRINT',    r'اطبع'),         
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'),  
        ('STRING',   r'"[^"]*"'),      
        ('ASSIGN',   r'='),            
        ('GT',       r'>'),            
        ('LT',       r'<'),            
        ('EQ',       r'=='),           
        ('END',      r';'),            
        ('SKIP',     r'[ \t]+'),       
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup != 'SKIP']

def run_interpreter(tokens):
    global variables
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

            # 1️⃣ عقل المنطق الشرطي
            if cmd == 'IF':
                var_name, op, threshold = stmt[1][1], stmt[2][0], float(stmt[3][1])
                message = stmt[5][1].strip('"')
                val = float(variables.get(var_name, 0))
                check = (val > threshold if op == 'GT' else val < threshold if op == 'LT' else val == threshold)
                if check: results.append(f"🎯 [قرار مَجال]: {message}")

            # 2️⃣ مصنع الواجهات الإلكترونية (الجنون الهيكلي)
            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "تطبيق مَجال")).strip('"')
                
                # ذكاء توزيع الخانات (الخريطة الهيكلية)
                raw_tabs = str(variables.get("الخانات", "الرئيسية، السلة، الحساب"))
                tabs = [t.strip() for t in raw_tabs.split('،')]
                
                if sys_type == "موقع":
                    # توليد أزرار التنقل السفلي بشكل آلي متناسق
                    nav_html = ""
                    for tab in tabs:
                        nav_html += f"""
                        <div class="flex flex-col items-center justify-center group cursor-pointer">
                            <div class="w-6 h-6 bg-gray-200 rounded-md mb-1 group-hover:bg-blue-500 transition-colors"></div>
                            <span class="text-[10px] font-bold text-gray-500 group-hover:text-blue-600">{tab}</span>
                        </div>"""

                    results.append(f"""
📱 [هندسة واجهة مستخدم - {name}]:
--------------------------------------------------
جاري توليد الموقع بـ ({len(tabs)}) أقسام سفلية احترافية...

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Tajawal', sans-serif; background: #f9fafb; }}
        .bottom-nav {{ box-shadow: 0 -5px 25px rgba(0,0,0,0.03); border-radius: 25px 25px 0 0; }}
    </style>
</head>
<body class="pb-24">
    <header class="bg-white p-6 shadow-sm sticky top-0 z-50 flex justify-between items-center">
        <div class="text-xl font-black text-blue-600 uppercase tracking-tighter">{name}</div>
        <div class="w-10 h-10 bg-gray-100 rounded-full"></div>
    </header>

    <main class="p-6 space-y-6">
        <div class="bg-gradient-to-br from-blue-600 to-blue-800 p-8 rounded-[2.5rem] text-white shadow-xl">
            <h2 class="text-3xl font-black mb-2 italic">مرحباً بك في {tabs[0]}</h2>
            <p class="opacity-80 text-sm font-light">تم تخصيص هذا الموقع الإلكتروني بناءً على رؤية المبرمج وسام ليكون واجهة عصرية وسريعة.</p>
        </div>

        <div class="grid grid-cols-2 gap-4">
            <div class="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
                <div class="w-10 h-10 bg-blue-50 rounded-xl mb-4"></div>
                <h4 class="font-bold">قسم {tabs[1] if len(tabs)>1 else "الخدمات"}</h4>
            </div>
            <div class="bg-white p-6 rounded-3xl shadow-sm border border-gray-100">
                <div class="w-10 h-10 bg-blue-50 rounded-xl mb-4"></div>
                <h4 class="font-bold">قسم {tabs[2] if len(tabs)>2 else "الإعدادات"}</h4>
            </div>
        </div>
    </main>

    <nav class="fixed bottom-0 w-full bg-white p-5 px-10 flex justify-around items-center bottom-nav border-t border-gray-100">
        {nav_html}
    </nav>
</body>
</html>
--------------------------------------------------
""")
            elif cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]

        except Exception as e:
            results.append(f"❌ خطأ في الهندسة البرمجية: {str(e)}")
    
    return "\n".join(results) if results else "✅ المحرك مستعد للبناء"
