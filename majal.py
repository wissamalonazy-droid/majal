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
    
    # تقسيم الكود إلى جمل برمجية بناءً على الفاصلة المنقوطة
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    for stmt in statements:
        try:
            cmd = stmt[0][0]

            # 1️⃣ معالجة تعريف المتغيرات (VAR)
            if cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]

            # 2️⃣ معالجة أوامر البناء (BUILD) - جوهر الجنون الإلكتروني
            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "براند مَجال")).strip('"')
                
                # 🎨 ميزة الألوان الحرة (المبرمج يكتب أي لون Hex أو اسم)
                user_color = str(variables.get("اللون", "#3b82f6")).strip('"')
                
                # 📱 ميزة توزيع الخانات الذكية
                raw_tabs = str(variables.get("الخانات", "الرئيسية، السلة، الحساب"))
                tabs = [t.strip() for t in raw_tabs.split('،')]
                
                # 🗺️ خريطة الأيقونات التلقائية
                icon_map = {
                    "الرئيسية": "🏠", "السلة": "🛒", "المتجر": "🛍️", 
                    "حسابي": "👤", "الحساب": "👤", "من نحن": "ℹ️", "اتصل بنا": "📞"
                }

                if sys_type == "موقع":
                    # توليد أزرار التنقل السفلي بناءً على الخانات والأيقونات
                    nav_html = "".join([f"""
                        <div class="flex flex-col items-center group cursor-pointer transition-all active:scale-90 opacity-70 hover:opacity-100">
                            <span class="text-xl mb-1">{icon_map.get(tab, "✨")}</span>
                            <span class="text-[9px] font-bold uppercase tracking-tighter">{tab}</span>
                        </div>""" for tab in tabs])
                    
                    results.append(f"""
🎨 [نظام مَجال 2.1.3 - هندسة الألوان والواجهات]:
--------------------------------------------------
هوية المشروع: {name} | لون الهوية المطبق: {user_color}

<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #050505; color: white; font-family: 'Tajawal', sans-serif; margin: 0; }}
        .accent-color {{ color: {user_color}; }}
        .accent-bg {{ background: {user_color}; }}
        .glass-panel {{ 
            background: rgba(255, 255, 255, 0.02); 
            backdrop-filter: blur(20px); 
            border: 1px solid {user_color}33;
            border-radius: 40px;
        }}
        .glow-effect {{ filter: drop-shadow(0 0 15px {user_color}44); }}
        .nav-footer {{ background: rgba(0,0,0,0.6); backdrop-filter: blur(25px); border-top: 1px solid rgba(255,255,255,0.05); }}
    </style>
</head>
<body class="pb-32 min-h-screen relative overflow-x-hidden">
    <nav class="p-8 flex justify-between items-center border-b border-white/5 sticky top-0 bg-[#050505]/80 backdrop-blur-md z-50">
        <div class="text-2xl font-black accent-color tracking-tighter uppercase glow-effect">{name}</div>
        <div class="w-10 h-10 glass-panel rounded-full flex items-center justify-center text-xs">🔔</div>
    </nav>

    <main class="p-8 text-center pt-20">
        <div class="inline-block px-5 py-2 rounded-full glass-panel text-[10px] accent-color mb-8 uppercase tracking-[0.4em] font-black border-none">
            Majal Digital Architecture
        </div>
        
        <h1 class="text-7xl font-black mb-10 tracking-tighter leading-none glow-effect">
            عالم <br><span class="accent-color italic">{name}</span>
        </h1>

        <div class="glass-panel p-10 text-right mt-16 relative overflow-hidden">
            <div class="absolute -right-10 -top-10 w-40 h-40 accent-bg opacity-10 rounded-full blur-3xl"></div>
            <div class="w-16 h-1 accent-bg mb-6 rounded-full glow-effect"></div>
            <h3 class="text-3xl font-black mb-4 italic">مرحباً بك في {tabs[0]}</h3>
            <p class="text-gray-500 text-sm leading-loose max-w-md">
                هذا الموقع الإلكتروني تم توليده بذكاء مَجال، حيث تم دمج اللون المخصص {user_color} مع هيكلة الخانات التي حددتها في الكود.
            </p>
        </div>
    </main>

    <nav class="fixed bottom-0 w-full p-6 px-10 flex justify-around items-center nav-footer z-50">
        {nav_html}
    </nav>
</body>
</html>
--------------------------------------------------
""")

            # 3️⃣ المنطق الشرطي (IF)
            elif cmd == 'IF':
                var_name, op, threshold = stmt[1][1], stmt[2][0], float(stmt[3][1])
                message = stmt[5][1].strip('"')
                val = float(variables.get(var_name, 0))
                check = (val > threshold if op == 'GT' else val < threshold if op == 'LT' else val == threshold)
                if check: results.append(f"🎯 [منطق مَجال]: {message}")

        except Exception as e:
            results.append(f"❌ خطأ برمجـي: {str(e)}")
    
    return "\n".join(results) if results else "✅ محرك مَجال مستعد للابتكار.."
