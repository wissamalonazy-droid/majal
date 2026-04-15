import re

# =========================
# المحلل اللغوي (Tokenizer) - نسخة المتجر 2.1
# =========================
def tokenize(code):
    # مصفوفة القواعد المحدثة لدعم أوامر التجارة الإلكترونية
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),      # الأرقام (دعم الفواصل العشرية للأسعار)
        ('STRING',   r'"[^"]*"'),          # النصوص (أسماء المنتجات)
        ('ASSIGN',   r'='),                # علامة التساوي
        ('END',      r';'),                # نهاية السطر
        ('OP',       r'[+\-*/]'),          # العمليات الحسابية
        
        # كلمات محجوزة لبناء المتاجر (Keywords)
        ('STORE',    r'تخزين'),             # أمر حفظ البيانات
        ('PRODUCT',  r'منتج'),             # تعريف منتج
        ('PRICE',    r'سعر'),              # تعريف سعر
        
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), # المتغيرات بالعربي والإنجليزي
        ('NEWLINE',  r'\n'),               # سطر جديد
        ('SKIP',     r'[ \t]+'),           # المسافات
        ('MISMATCH', r'.'),                # رموز غير معروفة
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

# سيتم إضافة الـ Interpreter (المفسر) في التحديث القادم لربطه بالقاعدة فعلياً
