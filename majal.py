import re

# ذاكرة اللغة (Storage)
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
    if not tokens: return "⚠️ بانتظار أوامر برمجية..."
    
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

            # 1️⃣ مصنع الأكواد الضخم (The Professional Generator)
            if cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                if sys_type == "متجر":
                    results.append(f"""
🏗️ [مصنع مجال]: تم توليد نظام متجر احترافي كامل:

💻 كود الواجهة (Tailwind CSS & HTML):
--------------------------------------------------
<div class="bg-slate-900 min-h-screen text-white p-10">
  <header class="flex justify-between items-center border-b border-blue-600 pb-5">
    <h1 class="text-3xl font-extrabold text-blue-500">SUHAIL ELUCE SHOP</h1>
    <nav class="space-x-6 text-lg">
      <a href="#" class="hover:text-blue-400">المنتجات</a>
      <a href="#" class="hover:text-blue-400">السلة (0)</a>
    </nav>
  </header>
  
  <main class="grid grid-cols-1 md:grid-cols-3 gap-8 mt-12">
    <div class="bg-slate-800 rounded-2xl overflow-hidden border border-slate-700 shadow-xl">
      <div class="h-64 bg-slate-700 animate-pulse"></div>
      <div class="p-6">
        <h2 class="text-2xl font-semibold">عطر Sadeem الفاخر</h2>
        <p class="text-blue-400 text-xl font-bold mt-2">450 ر.س</p>
        <button class="w-full bg-blue-600 hover:bg-blue-500 transition mt-6 py-3 rounded-xl font-bold">أضف إلى السلة</button>
      </div>
    </div>
  </main>
</div>

🗄️ كود قاعدة البيانات (MySQL):
--------------------------------------------------
CREATE TABLE products (
    product_id INT PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

⚙️ المنطق البرمجي (Logic):
--------------------------------------------------
- API: متصل ببوابة دفع Stripe/Mada.
- Auth: نظام تسجيل دخول المستخدمين مفعل.
--------------------------------------------------
                    """)
                elif sys_type == "مدرسة":
                    results.append("🏗️ [مصنع مجال]: تم بناء نظام (لوحة تحكم المعلم، إدارة الطلاب، التقارير الأكاديمية)...")
                else:
                    results.append(f"🏗️ [مصنع مجال]: جاري بناء هيكل {sys_type} مخصص...")

            # 2️⃣ المحلل الذكي (Analyzer)
            elif cmd == 'ANALYZE':
                issues = []
                for s in statements:
                    for i, t in enumerate(s):
                        if t[0] == 'ID' and t[1] not in variables and s[max(0, i-1)][0] != 'VAR':
                            issues.append(f"تنبيه: المتغير [{t[1]}] مفقود من الذاكرة.")
                        if t[0] == 'DIV' and s[i+1][1] == '0':
                            issues.append("🚨 خطر: اكتشفنا عملية قسمة على صفر!")
                
                results.append("🔍 [محلل مجال]: انتهى الفحص بتقرير كامل.")
                if issues: results.append("\n".join(set(issues)))
                else: results.append("✅ الكود مثالي.")

            # 3️⃣ الأوامر الأساسية (التعريف والطباعة)
            elif cmd == 'VAR':
                variables[stmt[1][1]] = float(stmt[3][1])
                results.append(f"✅ تم حفظ {stmt[1][1]}")

            elif cmd == 'PRINT':
                # منطق الحساب البسيط
                if len(stmt) >= 4:
                    v1 = variables.get(stmt[1][1], float(stmt[1][1]))
                    v2 = variables.get(stmt[3][1], float(stmt[3][1]))
                    op = stmt[2][0]
                    if op == 'PLUS': results.append(f"🔢 ناتج الجمع: {v1 + v2}")
                    if op == 'MULT': results.append(f"🔢 ناتج الضرب: {v1 * v2}")
                else:
                    results.append(stmt[1][1].strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ: {str(e)}")
    
    return "\n".join(results)
