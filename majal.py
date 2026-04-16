import re

# ذاكرة اللغة (Storage)
variables = {}

def tokenize(code):
    token_specification = [
        ('BUILD',    r'ابني'),         # أمر البناء التلقائي
        ('ANALYZE',  r'فحص'),         # أمر المحلل الذكي
        ('VAR',      r'عرف'),          # تعريف المتغيرات
        ('PRINT',    r'اطبع'),         # الطباعة
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), # الأسماء
        ('NUMBER',   r'\d+(\.\d+)?'),  # الأرقام
        ('STRING',   r'"[^"]*"'),      # النصوص
        ('ASSIGN',   r'='),            # مساواة
        ('PLUS',     r'\+'),           # جمع
        ('MINUS',    r'-'),           # طرح
        ('MULT',     r'\*'),           # ضرب
        ('DIV',      r'/'),            # قسمة
        ('GT',       r'أكبر_من'),      # مقارنة أكبر
        ('LT',       r'أصغر_من'),      # مقارنة أصغر
        ('END',      r';'),            # نهاية السطر
        ('SKIP',     r'[ \t]+'),       # مسافات
        ('NEWLINE',  r'\n'),           # سطر جديد
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "⚠️ بانتظار أوامر برمجية..."
    
    results = []
    statements = []
    current_stmt = []
    
    # تقسيم الكود إلى جمل برمجية
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    for stmt in statements:
        try:
            cmd = stmt[0][0]

            # 1️⃣ نظام البناء التلقائي (Generator)
            if cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                if sys_type == "متجر":
                    results.append("""🏗️ [مصنع مجال]: تم توليد كود متجر كامل:
------------------------------------------
• قاعدة البيانات: CREATE TABLE products (id, name, price);
• الواجهة: <section class='shop'>...</section>
• المنطق: يتم ربط السلة بمعالج الدفع تلقائياً.
------------------------------------------""")
                elif sys_type == "مدرسه":
                    results.append("🏗️ [مصنع مجال]: تم بناء نظام إدارة الطلاب والجداول والدرجات.")
                else:
                    results.append(f"🏗️ [مصنع مجال]: جاري توليد كود مخصص لـ {sys_type}...")

            # 2️⃣ المحلل الذكي (Static Analyzer)
            elif cmd == 'ANALYZE':
                issues = []
                for s in statements:
                    for i, t in enumerate(s):
                        # كشف المتغيرات غير المعرفة
                        if t[0] == 'ID' and t[1] not in variables and s[max(0, i-1)][0] != 'VAR':
                            issues.append(f"تنبيه: المتغير [{t[1]}] مستخدم بس ما عرفته!")
                        # كشف القسمة على صفر
                        if t[0] == 'DIV' and s[i+1][1] == '0':
                            issues.append("🚨 كارثة: فيه قسمة على صفر! الكود بينفجر.")
                
                if not issues:
                    results.append("🔍 [محلل مجال]: كودك نظيف وفخم، جاهز للإطلاق.")
                else:
                    results.append("🔍 [محلل مجال] وجد ملاحظات:\n" + "\n".join(set(issues)))

            # 3️⃣ تعريف المتغيرات (Variable Definition)
            elif cmd == 'VAR':
                var_name = stmt[1][1]
                var_value = float(stmt[3][1])
                variables[var_name] = var_value
                results.append(f"✅ تم حفظ [{var_name}] في الذاكرة بقيمة {var_value}")

            # 4️⃣ العمليات الحسابية والطباعة
            elif cmd == 'PRINT':
                if len(stmt) >= 4:
                    val1 = variables.get(stmt[1][1], float(stmt[1][1])) if stmt[1][0] in ['ID','NUMBER'] else 0
                    val2 = variables.get(stmt[3][1], float(stmt[3][1])) if stmt[3][0] in ['ID','NUMBER'] else 0
                    op = stmt[2][0]
                    
                    if op == 'PLUS': results.append(f"🔢 الناتج: {val1 + val2}")
                    elif op == 'MINUS': results.append(f"🔢 الناتج: {val1 - val2}")
                    elif op == 'MULT': results.append(f"🔢 الناتج: {val1 * val2}")
                    elif op == 'DIV': results.append(f"🔢 الناتج: {val1 / val2}" if val2 != 0 else "❌ خطأ في الحساب")
                    elif op == 'GT': results.append("✅ صح" if val1 > val2 else "❌ خطأ")
                else:
                    target = stmt[1][1]
                    if stmt[1][0] == 'STRING': results.append(target.strip('"'))
                    elif target in variables: results.append(f"قيمة {target} هي: {variables[target]}")
                    else: results.append(target)

        except Exception as e:
            results.append(f"❌ مشكلة في البرمجة: {str(e)}")
    
    return "\n".join(results)
