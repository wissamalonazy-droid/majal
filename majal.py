import re
variables = {}

def tokenize(code):
    token_specification = [
        ('BUILD',    r'ابني'),
        ('ANALYZE',  r'فحص'),
        ('VAR',      r'عرف'),
        ('PRINT',    r'اطبع'),
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'),
        ('STRING',   r'"[^"]*"'),
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('DIV',      r'/'),
        ('END',      r';'),
        ('SKIP',     r'[ \t]+'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup != 'SKIP']

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
            # 1. تطوير "ابني"
            if stmt[0][0] == 'BUILD':
                sys = stmt[1][1].strip('"')
                if sys == "متجر":
                    results.append("🏗️ [بناء مجال]: تم توليد قاعدة بيانات المتجر (المنتجات، السلال، المستخدمين).")
                elif sys == "مدرسة":
                    results.append("🏗️ [بناء مجال]: تم إنشاء نظام إداري كامل للمدرسة والفصول.")
                else:
                    results.append(f"🏗️ [بناء مجال]: جاري بناء نظام {sys}...")

            # 2. تطوير "المحلل" (كشف القسمة على صفر)
            elif stmt[0][0] == 'ANALYZE':
                for s in statements:
                    for i, t in enumerate(s):
                        if t[0] == 'DIV' and s[i+1][1] == '0':
                            results.append("🚨 [تحذير فحص]: انتبه! فيه محاولة قسمة على صفر، الكود بينفجر لو شغلته!")
                results.append("🔍 [محلل مجال]: انتهى الفحص.")

            elif stmt[0][0] == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]
                results.append(f"✅ تم تعريف {stmt[1][1]}")

        except: results.append("❌ خطأ في صياغة السطر")
    
    return "\n".join(results)
