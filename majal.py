import re

variables = {}

def tokenize(code):
    token_specification = [
        ('GENERATE', r'ابني_نظام'),   # أمر بناء كود تلقائي
        ('ANALYZE',  r'فحص'),         # أمر تحليل الكود
        ('VAR',      r'عرف'),
        ('PRINT',    r'اطبع'),
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'),
        ('NUMBER',   r'\d+'),
        ('ASSIGN',   r'='),
        ('END',      r';'),
        ('SKIP',     r'[ \t]+'),
    ]
    # ... (نفس منطق التوكنز السابق)
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup != 'SKIP']

def run_interpreter(tokens):
    if not tokens: return ""
    
    # ميزة (ابني_نظام): توليد كود برمجي كامل
    if tokens[0][0] == 'GENERATE':
        system_name = tokens[1][1]
        generated_code = f"""
        // تم بناء نظام {system_name} تلقائياً بواسطة مجال
        عرف {system_name}_حالة = 1 ;
        اطبع "نظام {system_name} جاهز للعمل" ;
        """
        return f"🏗️ تم توليد الهيكل البرمجي التالي:\n{generated_code}"

    # ميزة (فحص): تحليل الكود والبحث عن أخطاء منطقية
    if tokens[0][0] == 'ANALYZE':
        analysis_report = "🔍 تقرير فحص مجال:\n"
        if len(variables) == 0:
            analysis_report += "- تنبيه: الذاكرة فارغة، لم تقم بتعريف أي متغيرات بعد.\n"
        else:
            analysis_report += f"- ذاكرة اللغة تحتوي على {len(variables)} متغيرات.\n"
        return analysis_report

    return "💡 كود جاهز للمعالجة."
