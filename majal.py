import re

variables = {}

def run_interpreter(tokens):
    global variables
    results = []
    # ... (الجزء الخاص بالـ tokenize يبقى كما هو)
    
    for stmt in statements:
        try:
            cmd = stmt[0][0]
            if cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]
            
            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "متجر وسام")).strip('"')
                user_color = str(variables.get("اللون", "#3b82f6")).strip('"')
                desc = str(variables.get("وصف", "أفخم المنتجات بين يديك")).strip('"')

                if sys_type == "موقع":
                    results.append(f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/alpinejs@3.x.x/dist/cdn.min.js" defer></script>
    <style>
        body {{ background: #050505; color: white; font-family: 'Tajawal', sans-serif; }}
        .accent-color {{ color: {user_color}; }}
        .accent-bg {{ background: {user_color}; }}
        .glass {{ background: rgba(255,255,255,0.02); backdrop-filter: blur(20px); border: 1px solid rgba(255,255,255,0.05); }}
    </style>
</head>
<body x-data="{{ page: 'home', cart: [] }}">
    
    <nav class="p-6 flex justify-between items-center sticky top-0 bg-black/80 backdrop-blur-md z-50 border-b border-white/5">
        <div class="text-2xl font-black accent-color uppercase tracking-tighter" x-text="'{name}'"></div>
        <div class="flex gap-4">
            <button @click="page = 'cart'" class="relative p-2 glass rounded-full">
                🛒 <span class="absolute -top-1 -right-1 bg-red-600 text-[10px] px-1.5 rounded-full" x-text="cart.length"></span>
            </button>
        </div>
    </nav>

    <main class="p-6 pb-32">
        
        <template x-if="page === 'home'">
            <div class="space-y-8">
                <header class="text-center py-10">
                    <h1 class="text-5xl font-black mb-4 italic accent-color">المتجر</h1>
                    <p class="text-gray-500">{desc}</p>
                </header>
                <div class="grid grid-cols-2 gap-4">
                    <template x-for="i in [1,2,3,4]">
                        <div class="glass p-4 rounded-[2rem] text-center">
                            <div class="h-32 bg-white/5 rounded-2xl mb-4 flex items-center justify-center text-3xl">📦</div>
                            <h3 class="font-bold text-sm mb-2" x-text="'منتج متميز ' + i"></h3>
                            <button @click="cart.push(i)" class="accent-bg text-white text-[10px] px-4 py-2 rounded-full w-full font-black">إضافة للسلة</button>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="page === 'cart'">
            <div class="animate-fade-in">
                <h1 class="text-3xl font-black mb-8 accent-color">سلة المشتريات</h1>
                <template x-if="cart.length === 0">
                    <p class="text-gray-600 italic text-center py-20">سلتك فارغة حالياً..</p>
                </template>
                <div class="space-y-4">
                    <template x-for="item in cart">
                        <div class="glass p-4 rounded-2xl flex justify-between items-center">
                            <span x-text="'منتج رقم ' + item"></span>
                            <button @click="cart = cart.filter(i => i !== item)" class="text-red-500 text-xs">حذف</button>
                        </div>
                    </template>
                </div>
            </div>
        </template>

        <template x-if="page === 'about'">
            <div class="text-center py-20">
                <h1 class="text-3xl font-black mb-6 accent-color">عن {name}</h1>
                <p class="text-gray-400 leading-loose">{desc}</p>
            </div>
        </template>

        <template x-if="page === 'account'">
            <div class="glass p-10 rounded-[3rem] text-center">
                <div class="w-20 h-20 bg-white/10 rounded-full mx-auto mb-6 flex items-center justify-center text-4xl">👤</div>
                <h2 class="text-xl font-black mb-2">مرحباً بك يا مستخدم</h2>
                <p class="text-gray-500 text-xs">هنا يمكنك إدارة طلباتك وعنوانك.</p>
            </div>
        </template>

    </main>

    <nav class="fixed bottom-0 w-full p-6 flex justify-around bg-black/90 backdrop-blur-2xl border-t border-white/5">
        <button @click="page = 'home'" :class="page === 'home' ? 'accent-color opacity-100' : 'opacity-40'" class="flex flex-col items-center">
            <span class="text-xl">🏠</span><span class="text-[9px] font-bold uppercase">الرئيسية</span>
        </button>
        <button @click="page = 'cart'" :class="page === 'cart' ? 'accent-color opacity-100' : 'opacity-40'" class="flex flex-col items-center">
            <span class="text-xl">🛒</span><span class="text-[9px] font-bold uppercase">السلة</span>
        </button>
        <button @click="page = 'about'" :class="page === 'about' ? 'accent-color opacity-100' : 'opacity-40'" class="flex flex-col items-center">
            <span class="text-xl">ℹ️</span><span class="text-[9px] font-bold uppercase">من نحن</span>
        </button>
        <button @click="page = 'account'" :class="page === 'account' ? 'accent-color opacity-100' : 'opacity-40'" class="flex flex-col items-center">
            <span class="text-xl">👤</span><span class="text-[9px] font-bold uppercase">الحساب</span>
        </button>
    </nav>
</body>
</html>
""")
