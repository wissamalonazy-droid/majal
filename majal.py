import re
import sqlite3

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),       # أرقام
        ('STRING',   r'"[^"]*"'),           # نصوص
        ('PRINT',    r'اطبع'),              # أمر الطباعة
        ('VAR',      r'عرف'),               # تعريف متغير
        ('ASSIGN',   r'='),                 # مساواة
        ('PLUS',     r'\+'),                # جمع
        ('END',      r';'),                 # نهاية السطر
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), # أسماء المتغيرات
        ('SKIP',     r'[ \t]+'),
        ('NEWLINE',  r'\n'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP' or kind == 'NEWLINE': continue
        tokens.append((kind, value))
    return tokens

# مخزن مؤقت للمتغيرات (ذاكرة اللغة)
variables = {}

def run_interpreter(tokens):
    global variables
    if not tokens: return ""
    
    try:
        # أمر الطباعة: اطبع "نص" ;
        if tokens[0][0] == 'PRINT':
            return tokens[1][1].strip('"')
            
        # أمر التعريف: عرف س = 10 ;
        if tokens[0][0] == 'VAR':
            var_name = tokens[1][1]
            var_value = tokens[3][1]
            variables[var_name] = var_value
            return f"✅ تم تعريف {var_name} بقيمة {var_value}"
            
        return "💡 تم تحليل الكود بنجاح."
    except Exception as e:
        return f"❌ خطأ في التنفيذ: {str(e)}"
