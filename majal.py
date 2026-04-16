import re

variables = {}

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"[^"]*"'),
        ('PRINT',    r'اطبع'),
        ('VAR',      r'عرف'),
        ('GT',       r'أكبر_من'),
        ('LT',       r'أصغر_من'),
        ('PLUS',     r'\+'),
        ('MINUS',    r'-'),
        ('MULT',     r'\*'),
        ('DIV',      r'/'),
        ('ASSIGN',   r'='),
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
    global variables
    if not tokens: return ""
    try:
        # --- أمر التعريف ---
        if tokens[0][0] == 'VAR':
            var_name = tokens[1][1]
            var_value = float(tokens[3][1])
            variables[var_name] = var_value
            return f"✅ تم حفظ المتغير [{var_name}] بقيمة {var_value}"

        # --- أمر الطباعة والحساب الشامل ---
        if tokens[0][0] == 'PRINT':
            if len(tokens) >= 4:
                # جلب القيم (سواء كانت أرقام أو متغيرات من الذاكرة)
                val1 = variables.get(tokens[1][1], 0) if tokens[1][0] == 'ID' else float(tokens[1][1])
                val2 = variables.get(tokens[3][1], 0) if tokens[3][0] == 'ID' else float(tokens[3][1])
                op = tokens[2][0]

                if op == 'PLUS': return f"🔢 الناتج: {val1 + val2}"
                if op == 'MINUS': return f"🔢 الناتج: {val1 - val2}"
                if op == 'MULT': return f"🔢 الناتج: {val1 * val2}"
                if op == 'DIV': return f"🔢 الناتج: {val1 / val2}" if val2 != 0 else "❌ خطأ: قسمة على صفر!"
                if op == 'GT': return "✅ صح" if val1 > val2 else "❌ خطأ"
                if op == 'LT': return "✅ صح" if val1 < val2 else "❌ خطأ"

            return tokens[1][1].strip('"')
    except Exception as e:
        return f"❌ خطأ: {str(e)}"
