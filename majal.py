import re

variables = {}

def tokenize(code):
    token_specification = [
        ('BUILD',    r'ابني'),
        ('ANALYZE',  r'فحص'),
        ('VAR',      r'عرف'),
        ('PRINT',    r'اطبع'),
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'),
        ('NUMBER',   r'\d+'),
        ('ASSIGN',   r'='),
        ('PLUS',     r'\+'),
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
    # تقسيم التوكنز إلى جمل برمجية بناءً على الفاصلة المنقوطة (;)
    statements = []
    current_statement = []
    for token in tokens:
        current_statement.append(token)
        if token[0] == 'END':
            statements.append(current_statement)
            current_statement = []

    for stmt in statements:
        try:
            # --- منطق الفحص (الركيزة الأساسية) ---
            if stmt[0][0] == 'ANALYZE':
                issues = []
                # فحص المتغيرات المستخدمة في كامل الكود
                for s in statements:
                    for i, (kind, val) in enumerate(s):
                        if kind == 'ID' and val not in variables and s[max(0, i-1)][0] != 'VAR':
                            issues.append(f"تنبيه: المتغير [{val}] استخدمته بس ما عرفته!")
                
                if not issues:
                    results.append("🔍 [محلل مجال]: الكود سليم ومنطقي.")
                else:
                    results.append("🔍 [محلل مجال] وجد أخطاء:\n" + "\n".join(set(issues)))

            # --- منطق التعريف ---
            elif stmt[0][0] == 'VAR':
                var_name = stmt[1][1]
                variables[var_name] = float(stmt[3][1])
                results.append(f"✅ تم تعريف {var_name}")

            # --- منطق البناء ---
            elif stmt[0][0] == 'BUILD':
                results.append(f"🏗️ [بناء مجال]: جاري إنشاء هيكل لـ {stmt[1][1]}")

        except Exception as e:
            results.append(f"❌ خطأ في السطر: {str(e)}")

    return "\n".join(results) if results else "💡 تم استقبال الكود."
