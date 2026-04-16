import re

variables = {}

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"[^"]*"'),
        ('PRINT',    r'اطبع'),
        ('PLUS',     r'\+'),
        ('GT',       r'أكبر_من'),      # الرمز المجنون الجديد
        ('LT',       r'أصغر_من'),      # الرمز المجنون الجديد
        ('END',      r';'),
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'),
        ('SKIP',     r'[ \t]+'),
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'SKIP': continue
        tokens.append((kind, value))
    return tokens

def run_interpreter(tokens):
    if not tokens: return ""
    try:
        if tokens[0][0] == 'PRINT':
            # --- منطق المقارنة المجنون ---
            if len(tokens) >= 5:
                num1 = float(tokens[1][1])
                num2 = float(tokens[3][1])
                op = tokens[2][0]
                
                if op == 'GT': # أكبر من
                    return "✅ صح" if num1 > num2 else "❌ خطأ"
                if op == 'LT': # أصغر من
                    return "✅ صح" if num1 < num2 else "❌ خطأ"
                
                if op == 'PLUS': # الجمع السابق
                    return f"🔢 الناتج: {num1 + num2}"

            return tokens[1][1].strip('"')
    except Exception as e:
        return f"❌ خطأ في المنطق: {str(e)}"
