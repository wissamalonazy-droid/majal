import re

# ذاكرة اللغة (المكان اللي تنحفظ فيه المتغيرات)
variables = {}

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"[^"]*"'),
        ('PRINT',    r'اطبع'),
        ('VAR',      r'عرف'),
        ('ASSIGN',   r'='),
        ('END',      r';'),
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'),
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

def run_interpreter(tokens):
    global variables
    if not tokens: return ""
    
    try:
        # --- منطق أمر (عرف) ---
        if tokens[0][0] == 'VAR':
            var_name = tokens[1][1]
            var_value = tokens[3][1]
            variables[var_name] = var_value # تخزين في الذاكرة
            return f"✅ لغة مجال: تم حفظ المتغير [{var_name}] وقيمته ({var_value})"

        # --- منطق أمر (اطبع) ---
        if tokens[0][0] == 'PRINT':
            target_token_type = tokens[1][0]
            target_value = tokens[1][1]

            # 1. إذا كنت تطبع نص مباشر بين " "
            if target_token_type == 'STRING':
                return target_value.strip('"')

            # 2. إذا كنت تطبع اسم متغير (مثل: العمر)
            elif target_token_type == 'ID':
                if target_value in variables:
                    return f"القيمة المخزنة في {target_value} هي: {variables[target_value]}"
                else:
                    return f"❌ خطأ: المتغير [{target_value}] غير موجود في ذاكرة مجال."

        return "💡 كود صحيح، بانتظار أمر تنفيذ."
    except Exception as e:
        return f"❌ خطأ في التنفيذ: {str(e)}"
