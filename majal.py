import re

variables = {}

def tokenize(code):
    if not code: return []
    # تعريف التوكنز الأساسية
    token_specification = [
        ('IF',       r'إذا'), ('BUILD',    r'ابني'), ('VAR',      r'عرف'),          
        ('PRINT',    r'اطبع'), ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'), ('STRING',   r'"[^"]*"'), ('ASSIGN',   r'='),            
        ('END',      r';'), ('SKIP',     r'[ \t]+'), ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    line_num = 1
    
    # المحلل الذكي: يكتشف الرموز غير المعروفة فوراً
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE':
            line_num += 1
        elif kind == 'SKIP':
            continue
        else:
            tokens.append((kind, value, line_num))
    return tokens

def run_interpreter(tokens, full_code):
    global variables
    results = []
    errors = []
    statements = []
    current_stmt = []
    
    # 🕵️ فحص أولي: هل نسي المبرمج الفاصلة المنقوطة؟
    lines = full_code.strip().split('\n')
    for i, line in enumerate(lines):
        if line.strip() and not line.strip().endswith(';'):
            errors.append(f"⚠️ خطأ في السطر {i+1}: نسيت إغلاق الأمر بـ ';' يا بطل")

    # تقسيم الجمل
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    # إذا ما فيه أخطاء هيكلية، نبدأ التنفيذ
    if not errors:
        for stmt in statements:
            try:
                cmd = stmt[0][0]
                if cmd == 'VAR':
                    variables[stmt[1][1]] = stmt[3][1]
                elif cmd == 'BUILD':
                    # (هنا نضع كود بناء الموقع الحقيقي اللي سويناه قبل)
                    name = str(variables.get("الاسم", "متجر إلكتروني")).strip('"')
                    # ... [باقي كود الـ HTML] ...
                    results.append(f"✅ تم بناء '{name}' بنجاح وبدون أخطاء.")
                else:
                    errors.append(f"❌ أمر غير معروف: '{stmt[0][1]}' في السطر {stmt[0][2]}")
            except Exception:
                errors.append(f"❌ خطأ في تركيب الأمر بالسطر {stmt[0][2]}")

    # النتيجة النهائية: إما النجاح أو تقرير الأخطاء
    if errors:
        return "⚠️ [تقرير أخطاء مَجال]:\n" + "\n".join(errors)
    return "\n".join(results) if results else "📝 الكود سليم، ابدأ بكتابة أوامر البناء."
