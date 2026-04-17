import re

variables = {}

def tokenize(code):
    if not code: return []
    token_specification = [
        ('IF',       r'إذا'), ('BUILD',    r'ابني'), ('VAR',      r'عرف'),          
        ('PRINT',    r'اطبع'), ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'), ('STRING',   r'"[^"]*"'), ('ASSIGN',   r'='),            
        ('END',      r';'), ('SKIP',     r'[ \t]+'), ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "✅ المحرك جاهز للبناء الحقيقي"
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
                
                # جلب بيانات المنتجات الحقيقية من المبرمج
                raw_products = str(variables.get("المنتجات", "عطر سديم،عطر سنا،عطر طوق")).strip('"')
                product_list = [p.strip() for p in raw_products.split('،')]
                currency = str(variables.get("العملة", "ر.س")).strip('"')
                price = str(variables.get("السعر", "250")).strip('"')

                if sys_type == "موقع":
                    # تحويل المنتجات إلى كود JavaScript حقيقي للسلة
                    js_products = [{"id": i, "name": p, "price": price} for i, p in enumerate(product_list)]
                    
                    results.append(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        body {{ background: #050505; color: white; font-family: 'Tajawal', sans-serif; }}
        .accent-color {{ color: {user_color}; }}
        .accent-bg {{ background: {user_color}; }}
        .glass {{ background: rgba(255,255,255,0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.05); border-radius: 35px; }}
        .product-card {{ transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); }}
        .product-card:active {{ transform: scale(0.95); }}
    </style>
</head>
<body x-data="{{ 
    page: 'home', 
    cart: [], 
    products: {js_products},
    get cartTotal() {{ return this.cart.reduce((sum, item) => sum + parseFloat(item.price), 0); }}
}}">
    
    <nav class="p-6 flex justify-between items-center sticky top-0 bg-black/90 backdrop-blur-xl z-50 border-b border-white/5">
        <div class="text-2xl font-black accent-color uppercase tracking-tighter italic tracking-tight">{name}</div>
        <button @click="page = 'cart'" class="relative p-3 glass flex items-center gap-2">
            <span class="text-xs font-bold" x-text="cartTotal + ' {currency}'"></span>
            <div class="relative">
                🛒 <span class="absolute -top-3 -right-2 bg-red-600 text-[9px] px-1.5 py-0.5 rounded-full" x-text="cart.length"></span>
            </div>
        </button>
    </nav>

    <main class="p-6 pb-40">
        <template x-if="page === 'home'">
            <div>
                <header class="py-10 text-right">
                    <h1 class="text-5xl font-black accent-color italic leading-tight">استكشف <br>المجموعة</h1>
                    <p class="text-gray-500 mt-4 text-sm font-light">{desc}</p>
                </header>
                
                <div class="grid grid-cols-2 gap-5">
                    <template x-for="product in products" :key="product.id">
                        <div class="glass p-5 product-card flex flex-col justify-between">
                            <div class="h-40 bg-white/5 rounded-3xl mb-4 flex items-center justify-center text-5xl">✨</div>
                            <div class="text-right">
                                <h3 class="font-bold text-sm mb-1 text-white" x-text="product.name"></h3>
                                <p class="accent-color font-black text-xs mb-4" x-text="product.price + ' {currency}'"></p>
                            </div>
                            <button @click="cart.push(product)" class="accent-bg text-white text-[10px] py-3.5 rounded-2xl w-full font-black shadow-lg">إضافة للسلة</button>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="page === 'cart'">
            <div class="space-y-6">
                <h1 class="text-3xl font-black accent-color">الفاتورة</h1>
                <div class="space-y-3">
                    <template x-for="(item, index) in cart" :key="index">
                        <div class="glass p-5 flex justify-between items-center animate-in slide-in-from-right">
                            <div>
                                <p class="font-bold text-sm" x-text="item.name"></p>
                                <p class="text-[10px] opacity-50" x-text="item.price + ' {currency}'"></p>
                            </div>
                            <button @click="cart.splice(index, 1)" class="text-red-500 text-[10px] font-bold">إزالة</button>
                        </div>
                    </template>
                </div>
                
                <template x-if="cart.length > 0">
                    <div class="mt-10 p-6 glass border-dashed border-white/20">
                        <div class="flex justify-between mb-4">
                            <span class="text-gray-400">المجموع الأساسي</span>
                            <span x-text="cartTotal + ' {currency}'"></span>
                        </div>
                        <button class="accent-bg w-full py-5 rounded-2xl font-black text-lg">إتمام الطلب الآن</button>
                    </div>
                </template>

                <template x-if="cart.length === 0">
                    <div class="py-20 text-center text-gray-600 italic">السلة فارغة، ابدأ بالتسوق..</div>
                </template>
            </div>
        </template>

        <template x-if="page === 'account'">
            <div class="glass p-10">
                <h2 class="text-2xl font-black mb-8 text-center accent-color uppercase italic">Member Login</h2>
                <div class="space-y-4">
                    <input type="text" placeholder="اسم المستخدم أو الإيميل" class="w-full bg-white/5 p-5 rounded-2xl border border-white/10 text-sm outline-none focus:border-blue-500">
                    <input type="password" placeholder="كلمة المرور" class="w-full bg-white/5 p-5 rounded-2xl border border-white/10 text-sm outline-none focus:border-blue-500">
                    <button class="accent-bg w-full py-5 rounded-2xl font-black mt-4 shadow-xl">دخول الحساب</button>
                    <p class="text-center text-[10px] text-gray-500 uppercase mt-4">حماية كاملة للبيانات بواسطة MAJAL ENGINE</p>
                </div>
            </div>
        </template>
    </main>

    <nav class="fixed bottom-0 w-full p-6 flex justify-around bg-black/95 backdrop-blur-3xl border-t border-white/5 z-50">
        <button @click="page = 'home'" :class="page === 'home' ? 'accent-color' : 'opacity-30'" class="flex flex-col items-center"><span class="text-2xl mb-1">🏠</span><span class="text-[9px] font-bold">المتجر</span></button>
        <button @click="page = 'cart'" :class="page === 'cart' ? 'accent-color' : 'opacity-30'" class="flex flex-col items-center"><span class="text-2xl mb-1">🛒</span><span class="text-[9px] font-bold">السلة</span></button>
        <button @click="page = 'account'" :class="page === 'account' ? 'accent-color' : 'opacity-30'" class="flex flex-col items-center"><span class="text-2xl mb-1">👤</span><span class="text-[9px] font-bold">الحساب</span></button>
    </nav>
</body>
</html>
""")
        except Exception: continue
    return "\n".join(results)
