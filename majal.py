import re

# =========================
# تعريف الرموز (Constants)
# =========================
VERSION = "2.0.0"

# =========================
# المحلل اللغوي (Tokenizer)
# =========================
def tokenize(code):
    # مصفوفة القواعد (Patterns) لتعريف لغتك
    token_specification = [
        ('NUMBER',   r'\d+'),             # الأرقام
        ('STRING',   r'"[^"]*"'),         # النصوص بين علامات تنصيص
        ('ASSIGN',   r'='),               # علامة التساوي
        ('END',      r';'),               # نهاية السطر
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), # المتغيرات (دعم الحروف العربية)
        ('OP',       r'[+\-*/]'),         # العمليات الحسابية
        ('NEWLINE',  r'\n'),              # سطر جديد
        ('SKIP',     r'[ \t]+'),          # المسافات (يتم تجاهلها)
        ('MISMATCH', r'.'),               # أي رمز آخر غير معروف
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE' or kind == 'SKIP':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f'رمز غير معروف: {value}')
        tokens.append((kind, value))
    
    return tokens

# =========================
# المفسر البسيط (Interpreter)
# =========================
class Interpreter:
    def __init__(self):
        self.vars = {}

    def run(self, tokens):
        # حالياً المحرك يعيد التوكنز للتأكد من نجاح التحليل
        return tokens

# ملاحظة: هذا الملف يعمل كـ "مكتبة" يستدعيها ملف main.py
