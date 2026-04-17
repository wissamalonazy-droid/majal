import re

# ذاكرة اللغة
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
    
    # تقسيم الجمل البرمجية
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
                name = str(variables.get("الاسم", "متجر وسام")).strip('"')
                user_color = str(variables.get("اللون", "#3b82f6")).strip('"')
                desc = str(variables.get("وصف", "أفخم المنتجات بين يديك")).strip('"')

                if sys_type == "موقع":
                    # بناء الموقع المتكامل بالصفحات المنفصلة
                    results.append(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;900&display=swap" rel="stylesheet">
    <style>
        body {{ background: #050505; color: white; font-family: 'Tajawal', sans-serif; }}
        .accent-color {{ color: {user_color}; }}
        .accent-bg {{ background: {user_color}; }}
        .glass {{ background: rgba(255,255,255,0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.05); border-radius: 30px; }}
        .nav-footer {{ background: rgba(0,0,0,0.8); backdrop-filter: blur(25px); border-top: 1px solid rgba(255,255,255,0.05); }}
    </style>
</head>
<body x-data="{{ page: 'home', cart: [] }}">
    <nav class="p-6 flex justify-between items-center sticky top-0 bg-black/80 backdrop-blur-md z-50 border-b border-white/5">
        <div class="text-2xl font-black accent-color uppercase tracking-tighter">{name}</div>
        <button @click="page = 'cart'" class="relative p-3 glass">
            🛒 <span class="absolute -top-1 -right-1 bg-red-600 text-[10px] px-2 py-0.5 rounded-full" x-text="cart.length"></span>
        </button>
    </nav>

    <main class="p-6 pb-32">
        <template x-if="page === 'home'">
            <div>
                <header class="text-center py-10">
                    <h1 class="text-5xl font-black mb-4 italic accent-color">المتجر</h1>
                    <p class="text-gray-500">{desc}</p>
                </header>
                <div class="grid grid-cols-2 gap-4 mt-8">
                    <template x-for="i in [1,2,3,4]">
                        <div class="glass p-5 text-center">
                            <div class="h-32 bg-white/5 rounded-2xl mb-4 flex items-center justify-center text-4xl">📦</div>
                            <h3 class="font-bold mb-4" x-text="'منتج ' + i"></h3>
                            <button @click="cart.push(i)" class="accent-bg text-white text-xs py-3 rounded-2xl w-full font-black">إضافة للسلة</button>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="page === 'cart'">
            <div>
                <h1 class="text-3xl font-black mb-8 accent-color">السلة</h1>
                <div class="space-y-4">
                    <template x-for="item in cart">
                        <div class="glass p-6 flex justify-between items-center">
                            <span>منتج متميز #<span x-text="item"></span></span>
                            <button @click="cart = cart.filter(i => i !== item)" class="text-red-500 text-sm">حذف</button>
                        </div>
                    </template>
                    <template x-if="cart.length === 0">
                        <p class="text-center text-gray-600 py-20 italic">السلة فارغة..</p>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="page === 'account'">
            <div class="glass p-12 text-center">
                <div class="w-20 h-20 bg-white/10 rounded-full mx-auto mb-6 flex items-center justify-center text-4xl">👤</div>
                <h2 class="text-2xl font-black">حساب وسام</h2>
                <p class="text-gray-500 mt-2">مرحباً بك في لوحة التحكم الخاصة بك.</p>
            </div>
        </template>
    </main>

    <nav class="fixed bottom-0 w-full p-6 flex justify-around nav-footer z-50">
        <button @click="page = 'home'" :class="page === 'home' ? 'accent-color' : 'opacity-40'" class="flex flex-col items-center">
            <span class="text-2xl mb-1">🏠</span><span class="text-[10px] font-black">الرئيسية</span>
        </button>
        <button @click="page = 'cart'" :class="page === 'cart' ? 'accent-color' : 'opacity-40'" class="flex flex-col items-center">
            <span class="text-2xl mb-1">🛒</span><span class="text-[10px] font-black">السلة</span>
        </button>
        <button @click="page = 'account'" :class="page === 'account' ? 'accent-color' : 'opacity-40'" class="flex flex-col items-center">
            <span class="text-2xl mb-1">👤</span><span class="text-[10px] font-black">الحساب</span>
        </button>
    </nav>
</body>
</html>
""")
        except Exception as e:
            results.append(f"❌ خطأ: {str(e)}")
            
    return "\n".join(results) if results else "✅ تم تنفيذ العمليات"
