import re

variables = {}

def tokenize(code):
    # مفسر الرموز المطور ليكون أكثر مرونة مع المسافات
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"[^"]*"'),
        ('PRINT',    r'اطبع'),
        ('VAR',      r'عرف'),
        ('GT',       r'أكبر_من'),
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
    if not tokens: return "⚠️ المحرك لم يستلم أي كود."
    
    try:
        # --- أمر التعريف (عرف) ---
        if tokens[0][0] == 'VAR':
            if len(tokens) >= 4:
                var_name = tokens[1][1]
                var_value = float(tokens[3][1])
                variables[var_name] = var_value
                return f"✅ تم حفظ المتغير [{var_name}] في الذاكرة بقيمة {var_value}"
            else:
                return "❌ خطأ في صياغة أمر التعريف. مثال: عرف س = 10 ;"

        # --- أمر الطباعة والمقارنة (اطبع) ---
        if tokens[0][0] == 'PRINT':
            # حالة المقارنة: اطبع س أكبر_من 500 ;
            if len(tokens) >= 4 and tokens[2][0] == 'GT':
                # جلب القيمة من الذاكرة أو استخدام الرقم مباشرة
                val1 = variables.get(tokens[1][1], 0) if tokens[1][0] == 'ID' else float(tokens[1][1])
                val2 = float(tokens[3][1])
                
                if val1 > val2:
                    return f"✅ صح: {val1} فعلاً أكبر من {val2}"
                else:
                    return f"❌ خطأ: {val1} ليست أكبر من {val2}"

            # حالة طباعة نص أو متغير عادي
            if tokens[1][0] == 'STRING': return tokens[1][1].strip('"')
            if tokens[1][1] in variables: return f"القيمة هي: {variables[tokens[1][1]]}"
            return tokens[1][1]

        return "💡 كود صحيح، لكنه لا يحتوي على أمر (عرف) أو (اطبع)."
    except Exception as e:
        return f"❌ خطأ فني: {str(e)}"
