import re
import sqlite3

# =========================
# المحلل اللغوي (Tokenizer)
# =========================
def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"[^"]*"'),
        ('END',      r';'),
        # الكلمات المحجوزة للمتجر
        ('STORE',    r'تخزين'),
        ('PRODUCT',  r'منتج'),
        ('PRICE',    r'سعر'),
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'),
        ('SKIP',     r'[ \t]+'),
        ('NEWLINE',  r'\n'),
        ('MISMATCH', r'.'),
    ]
    
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE' or kind == 'SKIP': continue
        elif kind == 'MISMATCH': raise RuntimeError(f'رمز غير معروف: {value}')
        tokens.append((kind, value))
    return tokens

# =========================
# المفسر (Interpreter) لعمليات المتجر
# =========================
def run_interpreter(tokens):
    # إذا كان الكود يبدأ بكلمة "تخزين"
    if tokens[0][0] == 'STORE':
        try:
            # استخراج اسم المنتج والسعر من التوكنز
            product_name = tokens[2][1].strip('"') # الكلمة الثالثة هي الاسم
            product_price = float(tokens[4][1])    # الكلمة الخامسة هي السعر
            
            # الاتصال بقاعدة البيانات وحفظ المنتج
            conn = sqlite3.connect('majal_store.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (product_name, product_price))
            conn.commit()
            conn.close()
            
            return f"✅ تم حفظ المنتج ({product_name}) بسعر ({product_price}) في قاعدة بيانات المتاجر!"
        except Exception as e:
            return f"❌ فشل التخزين: تأكد من صياغة الأمر بشكل صحيح."
    
    return "💡 تم تحليل الكود بنجاح، لكن لا يوجد أمر تنفيذ."
