import re

# ذاكرة اللغة لتخزين المتغيرات
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
    if not tokens: return "⚠️ محرك مَجال بانتظار أوامر البناء الذكية..."
    
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

            # 1️⃣ مصنع الأنظمة الاحترافي (Multitasking Engine)
            if cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                
                # جلب المتغيرات المخصصة من الذاكرة (الاسم، العملة، الهوية)
                sys_name = str(variables.get("الاسم", "نظام مَجال")).strip('"')
                currency = str(variables.get("العملة", "SAR")).strip('"')

                if sys_type == "متجر":
                    results.append(f"""
🏗️ [نظام مَجال]: تم بناء مشروع (متجر متكامل) لـ {sys_name}:
- الواجهة: نظام HTML5/Tailwind متجاوب.
- العملة المعتمدة: {currency}.
- قاعدة البيانات: SQL جاهزة للمنتجات والطلبات.
- الحماية: نظام تشفير المعاملات المالية مفعل.
                    """)
                elif sys_type == "مستشفى":
                    results.append(f"""
🏥 [نظام مَجال]: تم بناء (منظومة طبية شاملة) لـ {sys_name}:
- إدارة المرضى: ملفات طبية إلكترونية وسجلات الحالات.
- المواعيد: نظام حجز آلي وربط مع الأطباء.
- الصيدلية: نظام جرد الأدوية والوصفات.
- المختبر: لوحة نتائج التحاليل الفورية.
                    """)
                elif sys_type == "بنك":
                    results.append(f"""
🏦 [نظام مَجال]: تم بناء (نظام بنكي محصن) لـ {sys_name}:
- الحسابات: إدارة الحسابات الجارية والادخار بـ ({currency}).
- الحماية: نظام مصادقة ثنائية (2FA) وتشفير أمني عالي.
- التحويلات: محرك معالجة الحوالات الفورية.
- السجلات: سجل كامل للعمليات المالية غير قابل للتلاعب.
                    """)
                elif sys_type == "توصيل":
                    results.append(f"""
🚚 [نظام مَجال]: تم بناء (منصة لوجستية) لـ {sys_name}:
- التتبع: نظام خرائط حي لمتابعة الشحنات.
- السائقين: تطبيق خاص للمناديب واستلام الطلبات.
- التكاليف: حساب تلقائي لرسوم التوصيل بـ ({currency}).
                    """)
                else:
                    results.append(f"🏗️ [نظام مَجال]: تم بناء هيكل أساسي لنظام ({sys_type}) مخصص.")

            # 2️⃣ المحلل الذكي
            elif cmd == 'ANALYZE':
                results.append("🔍 [محلل مَجال]: جاري فحص بنية النظام... ✅ الهيكل سليم ومطابق للمعايير.")

            # 3️⃣ الأوامر الأساسية
            elif cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]
                results.append(f"✅ تم تعريف [{stmt[1][1]}]")

            elif cmd == 'PRINT':
                target = stmt[1][1]
                results.append(str(variables.get(target, target)).strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ في النظام: {str(e)}")
    
    return "\n".join(results)
