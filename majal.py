import re

variables = {}

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"[^"]*"'),
        ('PRINT',    r'اطبع'),
        ('VAR',      r'عرف'),
        ('ASSIGN',   r'='),
        ('PLUS',     r'\+'), # علامة الجمع
        ('MINUS',    r'\-'), # علامة الطرح
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
        # --- تطوير أمر (عرف) ليدعم الحساب البسيط ---
        if tokens[0][0] == 'VAR':
            var_name = tokens[1][1]
            
            # إذا كان الأمر: عرف س = 10 + 20 ;
            if len(tokens) >= 6 and tokens[4][0] == 'PLUS':
                val1 = float(tokens[3][1])
                val2 = float(tokens[5][1])
                result = val1 + val2
                variables[var_name] = result
                return f"✅ تم الحساب: {var_name} أصبح {result}"
            
            # إذا كان تعريف عادي: عرف س = 10 ;
            else:
                variables[var_name] = tokens[3][1]
                return f"✅ تم حفظ {var_name}"

        # --- أمر (اطبع) ---
        if tokens[0][0] == 'PRINT':
            target = tokens[1][1]
            if tokens[1][0] == 'STRING': return target.strip('"')
            if target in variables: return str(variables[target])
            return f"❌ {target} غير معرف"

        return "💡 كود سليم"
    except Exception as e:
        return f"❌ خطأ: {str(e)}"
