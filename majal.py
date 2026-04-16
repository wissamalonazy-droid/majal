import re

# ذاكرة اللغة (لتعريف المتغيرات)
variables = {}

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),       # الأرقام
        ('STRING',   r'"[^"]*"'),           # النصوص
        ('PRINT',    r'اطبع'),              # أمر الطباعة
        ('PLUS',     r'\+'),                # علامة الجمع
        ('END',      r';'),                 # نهاية السطر
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), # أسماء المتغيرات
        ('SKIP',     r'[ \t]+'),            # مسافات
        ('NEWLINE',  r'\n'),                # سطر جديد
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
        # --- منطق أمر (اطبع) ---
        if tokens[0][0] == 'PRINT':
            
            # 1. حالة الحساب الديناميكي (رقم + رقم)
            # نتحقق لو السطر فيه: اطبع | رقم | + | رقم | ;
            if len(tokens) >= 5 and tokens[2][0] == 'PLUS':
                if tokens[1][0] == 'NUMBER' and tokens[3][0] == 'NUMBER':
                    # تحويل النصوص لأرقام حقيقية
                    num1 = float(tokens[1][1])
                    num2 = float(tokens[3][1])
                    result = num1 + num2
                    # إرجاع النص النهائي للمستخدم
                    return f"🔢 لغة مجال تقول: ناتج {num1} + {num2} يساوي ({result})"
            
            # 2. حالة طباعة نص عادي " "
            if tokens[1][0] == 'STRING':
                return tokens[1][1].strip('"')
            
            # 3. حالة طباعة متغير من الذاكرة
            target = tokens[1][1]
            if target in variables:
                return f"قيمة {target} هي: {variables[target]}"
            
            # افتراضي: طباعة القيمة كما هي
            return tokens[1][1]

        return "💡 تم تحليل الكود."
    except Exception as e:
        return f"❌ خطأ تقني في المعالج: {str(e)}"
