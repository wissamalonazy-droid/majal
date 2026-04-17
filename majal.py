import re

variables = {}

def tokenize(code):
    if not code: return []
    token_specification = [
        ('IF',       r'إذا'), ('BUILD',    r'ابني'), ('VAR',      r'عرف'),          
        ('PRINT',    r'اطبع'), ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'), ('STRING',   r'"[^"]*"'), ('ASSIGN',   r'='),            
        ('GT',       r'>'), ('LT',       r'<'), ('EQ',       r'=='),           
        ('END',      r';'), ('SKIP',     r'[ \t]+'), ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "✅ المحرك مستعد"
    results = []
    statements = []
    current_stmt = []
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt); current_stmt = []

    for stmt in statements:
        try:
            cmd = stmt[0][0]
            if cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]
            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "متجر إلكتروني")).strip('"')
                user_color = str(variables.get("اللون", "#3b82f6")).strip('"')
                desc = str(variables.get("وصف", "أفخم المنتجات")).strip('"')

                if sys_type == "موقع":
                    results.append(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        body {{ background: #050505; color: white; font-family: 'Tajawal', sans-serif; }}
        .accent-color {{ color: {user_color}; }}
        .accent-bg {{ background: {user_color}; }}
        .glass {{ background: rgba(255,255,255,0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.05); border-radius: 30px; }}
        [x-cloak] {{ display: none !important; }}
    </style>
</head>
<body x-data="{{ page: 'home', cart: [], added: false }}">
    
    <nav class="p-6 flex justify-between items-center sticky top-0 bg-black/80 backdrop-blur-md z-50 border-b border-white/5">
        <div class="text-2xl font-black accent-color uppercase tracking-tighter">{name}</div>
        <button @click="page = 'cart'" class="relative p-3 glass transition-transform active:scale-90">
            🛒 <span class="absolute -top-1 -right-1 bg-red-600 text-[10px] px-2 py-0.5 rounded-full" x-text="cart.length"></span>
        </button>
    </nav>

    <main class="p-6 pb-32">
        <template x-if="page === 'home'">
            <div class="animate-in fade-in duration-500">
                <header class="text-center py-10">
                    <h1 class="text-5xl font-black mb-4 italic accent-color">المجموعة</h1>
                    <p class="text-gray-500 text-sm px-10">{desc}</p>
                </header>
                <div class="grid grid-cols-2 gap-4">
                    <template x-for="i in [1,2,3,4]">
                        <div class="glass p-5 text-center transition-all hover:border-white/20">
                            <div class="h-32 bg-white/5 rounded-2xl mb-4 flex items-center justify-center text-4xl">🛍️</div>
                            <h3 class="font-bold mb-4 text-xs" x-text="'منتج حصري ' + i"></h3>
                            <button @click="cart.push(i); added = true; setTimeout(() => added = false, 1000)" 
                                    :class="added ? 'bg-green-600' : 'accent-bg'"
                                    class="text-white text-[10px] py-3 rounded-2xl w-full font-black transition-colors duration-300">
                                <span x-text="added ? 'تمت الإضافة ✅' : 'إضافة للسلة'"></span>
                            </button>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="page === 'cart'">
            <div class="space-y-6">
                <h1 class="text-3xl font-black accent-color">سلة المشتريات</h1>
                <template x-for="item in cart">
                    <div class="glass p-6 flex justify-between items-center">
                        <span class="font-bold">منتج رقم <span x-text="item"></span></span>
                        <button @click="cart = cart.filter(i => i !== item)" class="text-red-500 text-xs font-bold border border-red-500/20 px-3 py-1 rounded-lg">حذف</button>
                    </div>
                </template>
                <template x-if="cart.length === 0">
                    <div class="py-20 text-center opacity-30 italic">السلة خالية..</div>
                </template>
            </div>
        </template>

        <template x-if="page === 'about'">
            <div class="py-20 text-center space-y-6">
                <div class="w-20 h-20 accent-bg rounded-3xl mx-auto flex items-center justify-center text-3xl shadow-lg shadow-blue-900/20">✨</div>
                <h1 class="text-4xl font-black accent-color uppercase tracking-widest italic">قصتنا</h1>
                <p class="text-gray-400 leading-relaxed max-w-xs mx-auto text-sm">{desc}</p>
            </div>
        </template>

        <template x-if="page === 'account'">
            <div class="glass p-10 text-center">
                <div class="w-20 h-20 bg-white/5 rounded-full mx-auto mb-6 flex items-center justify-center text-4xl">👤</div>
                <h2 class="text-xl font-black mb-4">تسجيل الدخول</h2>
                <div class="space-y-3">
                    <div class="bg-white/5 p-4 rounded-2xl text-right text-gray-500 text-xs">البريد الإلكتروني</div>
                    <div class="bg-white/5 p-4 rounded-2xl text-right text-gray-500 text-xs">كلمة المرور</div>
                    <button class="accent-bg w-full py-4 rounded-2xl font-black mt-4">دخول</button>
                </div>
            </div>
        </template>
    </main>

    <nav class="fixed bottom-0 w-full p-6 flex justify-around bg-black/90 backdrop-blur-3xl border-t border-white/5 z-50">
        <button @click="page = 'home'" :class="page === 'home' ? 'accent-color' : 'opacity-30'" class="flex flex-col items-center"><span class="text-2xl mb-1">🏠</span><span class="text-[9px] font-bold">الرئيسية</span></button>
        <button @click="page = 'cart'" :class="page === 'cart' ? 'accent-color' : 'opacity-30'" class="flex flex-col items-center"><span class="text-2xl mb-1">🛒</span><span class="text-[9px] font-bold">السلة</span></button>
        <button @click="page = 'about'" :class="page === 'about' ? 'accent-color' : 'opacity-30'" class="flex flex-col items-center"><span class="text-2xl mb-1">ℹ️</span><span class="text-[9px] font-bold">من نحن</span></button>
        <button @click="page = 'account'" :class="page === 'account' ? 'accent-color' : 'opacity-30'" class="flex flex-col items-center"><span class="text-2xl mb-1">👤</span><span class="text-[9px] font-bold">الحساب</span></button>
    </nav>
</body>
</html>
""")
        except Exception: continue
    return "\n".join(results)

