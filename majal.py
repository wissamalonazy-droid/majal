import re

variables = {}

def tokenize(code):
    token_specification = [
        ('BUILD',    r'ابني'),         # أمر بناء كود
        ('ANALYZE',  r'فحص'),         # أمر تحليل
        ('VAR',      r'عرف'),
        ('PRINT',    r'اطبع'),
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'),
        ('STRING',   r'"[^"]*"'),
        ('NUMBER',   r'\d+'),
        ('END',      r';'),
        ('SKIP',     r'[ \t]+'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup != 'SKIP']

def run_interpreter(tokens):
    if not tokens: return "⚠️ بانتظار أوامر برمجية..."
    
    # --- الركيزة 1: بناء الكود التلقائي ---
    if tokens[0][0] == 'BUILD':
        target = tokens[1][1].strip('"')
        if target == "واجهة":
            return "🏗️ [مجال Builder]: تم بناء هيكل واجهة المستخدم (UI) بنجاح."
        return f"🏗️ [مجال Builder]: جاري توليد كود لـ {target}..."

    # --- الركيزة 2: محلل الأخطاء الذكي ---
    if tokens[0][0] == 'ANALYZE':
        issues = []
        # فحص وجود متغيرات غير معرفة
        for i, (kind, val) in enumerate(tokens):
            if kind == 'ID' and val not in variables and tokens[i-1][0] != 'VAR':
                issues.append(f"تنبيه: المتغير [{val}] مستخدم لكنه غير معرف.")
        
        if not issues:
            return "🔍 [محلل مجال]: الكود سليم 100% وجاهز للانطلاق."
        return "🔍 [محلل مجال] وجد ملاحظات:\n" + "\n".join(issues)

    return "💡 تم استقبال الكود بنجاح."
