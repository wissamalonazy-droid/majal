import re

# ذاكرة اللغة لتخزين المتغيرات
variables = {}

def tokenize(code):
    if not code: return []
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
        ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "✅ المحرك مستعد للبناء"
    
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
            if not stmt: continue
            cmd = stmt[0][0]

            if cmd == 'VAR':
                if len(stmt) >= 4:
                    variables[stmt[1][1]] = stmt[3][1]

            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "براند مَجال")).strip('"')
                user_color = str(variables.get("اللون", "#3b82f6")).strip('"')
                
                # معالجة الخانات والأيقونات
                raw_tabs = str(variables.get("الخانات", "الرئيسية، السلة، الحساب"))
                tabs = [t.strip() for t in raw_tabs.split('،')]
                icon_map = {
                    "الرئيسية": "🏠", "السلة": "🛒", "المتجر": "🛍️", 
                    "حسابي": "👤", "الحساب": "👤", "من نحن": "ℹ️", "اتصل بنا": "📞"
                }

                if sys_type == "موقع":
                    # 1️⃣ توليد الأقسام الحقيقية (الأعصاب)
                    sections_html = ""
                    for i, tab in enumerate(tabs):
                        bg_style = f"background: linear-gradient(to bottom, #050505, {user_color}05);" if i % 2 == 0 else ""
                        sections_html += f"""
                        <section id="section-{i}" class="min-h-screen flex items-center justify-center p-6 border-b border-white/5" style="{bg_style}">
                            <div class="glass-panel p-12 text-center glow-effect w-full max-w-xl">
                                <span class="text-7xl mb-6 block">{icon_map.get(tab, "✨")}</span>
                                <h2 class="text-4xl font-black mb-4 italic accent-color">{tab}</h2>
                                <p class="text-gray-500 leading-relaxed font-light">مرحباً بك في صفحة {tab}. تم تخصيص هذا المحتوى لـ {name} بناءً على هندسة "مَجال" الذكية.</p>
                            </div>
                        </section>"""

                    # 2️⃣ توليد شريط التنقل مع روابط الربط (#)
                    nav_html = ""
                    for i, tab in enumerate(tabs):
                        nav_html += f"""
                        <a href="#section-{i}" class="flex flex-col items-center group transition-all active:scale-90 opacity-60 hover:opacity-100 no-underline text-white">
                            <span class="text-xl mb-1 group-hover:scale-110 transition-transform">{icon_map.get(tab, "✨")}</span>
                            <span class="text-[9px] font-bold uppercase tracking-tighter">{tab}</span>
                        </a>"""
                    
                    results.append(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl" style="scroll-behavior: smooth;">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #050505; color: white; font-family: 'Tajawal', sans-serif; margin: 0; }}
        .accent-color {{ color: {user_color}; }}
        .glass-panel {{ background: rgba(255, 255, 255, 0.02); backdrop-filter: blur(20px); border: 1px solid {user_color}33; border-radius: 40px; }}
        .glow-effect {{ filter: drop-shadow(0 0 15px {user_color}44); }}
        .nav-footer {{ background: rgba(0,0,0,0.8); backdrop-filter: blur(25px); border-top: 1px solid rgba(255,255,255,0.05); }}
    </style>
</head>
<body class="relative">
    <nav class="p-8 flex justify-between items-center border-b border-white/5 sticky top-0 bg-[#050505]/90 backdrop-blur-md z-50">
        <div class="text-2xl font-black accent-color tracking-tighter uppercase glow-effect">{name}</div>
        <div class="w-10 h-10 glass-panel rounded-full flex items-center justify-center text-xs">🔔</div>
    </nav>

    <main>
        {sections_html}
    </main>

    <nav class="fixed bottom-0 w-full p-6 px-10 flex justify-around items-center nav-footer z-50 shadow-[0_-10px_30px_rgba(0,0,0,0.5)]">
        {nav_html}
    </nav>
</body>
</html>
""")
            elif cmd == 'IF':
                var_name, op, threshold = stmt[1][1], stmt[2][0], float(stmt[3][1])
                message = stmt[5][1].strip('"')
                val = float(variables.get(var_name, 0))
                check = (val > threshold if op == 'GT' else val < threshold if op == 'LT' else val == threshold)
                if check: results.append(f"🎯 [منطق مَجال]: {message}")

        except Exception as e:
            results.append(f"❌ خطأ: {str(e)}")
            
    return "\n".join(results) if results else "✅ تم تنفيذ البناء بنجاح"
