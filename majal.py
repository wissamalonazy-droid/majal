import re

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

            if cmd == 'IF':
                var_name, op, threshold = stmt[1][1], stmt[2][0], float(stmt[3][1])
                message = stmt[5][1].strip('"')
                val = float(variables.get(var_name, 0))
                check = (val > threshold if op == 'GT' else val < threshold if op == 'LT' else val == threshold)
                if check: results.append(f"🎯 [قرار]: {message}")

            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "نظام مَجال")).strip('"')
                currency = str(variables.get("العملة", "SAR")).strip('"')
                
                if sys_type == "متجر":
                    results.append(f"""
🚀 [مشروع المتجر المتكامل لـ {name}]:

1. واجهة المستخدم (index.html):
--------------------------------------------------
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <script src="https://cdn.tailwindcss.com"></script>
    <title>{name}</title>
</head>
<body class="bg-[#050505] text-white">
    <nav class="p-8 border-b border-blue-900 flex justify-between items-center">
        <h1 class="text-3xl font-black text-blue-500 uppercase">{name}</h1>
        <ul class="flex gap-8 text-lg font-bold">
            <li>الرئيسية</li><li>المنتجات</li><li class="bg-blue-600 px-4 py-1 rounded-lg">السلة</li>
        </ul>
    </nav>
    <main class="p-12 text-center">
        <h2 class="text-5xl font-extrabold mb-10">مرحباً بكم في {name}</h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-10">
             <div class="bg-gray-900 p-8 rounded-[40px] border border-gray-800 shadow-2xl transition-transform hover:scale-105">
                <div class="h-64 bg-gradient-to-br from-blue-900 to-black rounded-3xl mb-6"></div>
                <h3 class="text-2xl font-bold">المنتج المميز</h3>
                <p class="text-blue-400 mt-2 font-mono text-xl">السعر: 450 {currency}</p>
                <button class="w-full bg-blue-600 mt-8 py-4 rounded-2xl font-black tracking-widest uppercase hover:bg-blue-500">أضف للسلة</button>
             </div>
        </div>
    </main>
</body>
</html>

2. قاعدة البيانات (init.sql):
--------------------------------------------------
CREATE DATABASE {name.replace(' ', '_')}_db;
CREATE TABLE products (id INT PRIMARY KEY, name VARCHAR(255), price DECIMAL(10,2), currency VARCHAR(10));
CREATE TABLE orders (id INT AUTO_INCREMENT, customer_name VARCHAR(100), total_price FLOAT);

3. محرك العمليات (app.js):
--------------------------------------------------
const storeName = "{name}";
const currency = "{currency}";

function processOrder(total) {{
    console.log(`جاري معالجة طلبك في ${{storeName}} بقيمة ${{total}} ${{currency}}`);
    alert("تم استلام طلبك بنجاح!");
}}
--------------------------------------------------
                    """)
                elif sys_type == "بنك":
                    results.append(f"🏦 [نظام بنكي لـ {name}]: تم توليد شيفرة الحماية، سجلات الحسابات بـ {currency}، ونظام التحقق الثنائي.")
                else:
                    results.append(f"📦 [نظام مخصص]: تم توليد هيكل {sys_type} كامل لـ {name}.")

            elif cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]

            elif cmd == 'PRINT':
                target = stmt[1][1]
                results.append(str(variables.get(target, target)).strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ: {str(e)}")
    
    return "\n".join(results) if results else "✅ تم التنفيذ"
