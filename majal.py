import re
import sqlite3

def tokenize(code):
    token_specification = [
        ('NUMBER',   r'\d+(\.\d+)?'),
        ('STRING',   r'"[^"]*"'),
        ('END',      r';'),
        ('STORE',    r'تخزين'),
        ('DISPLAY',  r'عرض'),              # أمر جديد للعرض
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

def run_interpreter(tokens):
    if not tokens: return "لا يوجد كود للتنفيذ"
    
    # حالة التخزين
    if tokens[0][0] == 'STORE':
        try:
            product_name = tokens[2][1].strip('"')
            product_price = float(tokens[4][1])
            conn = sqlite3.connect('majal_store.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO products (name, price) VALUES (?, ?)', (product_name, product_price))
            conn.commit()
            conn.close()
            return f"✅ تم حفظ المنتج ({product_name}) بسعر ({product_price})"
        except: return "❌ خطأ في صياغة أمر التخزين"

    # حالة العرض (الجديدة)
    if tokens[0][0] == 'DISPLAY':
        conn = sqlite3.connect('majal_store.db')
        cursor = conn.cursor()
        cursor.execute('SELECT name, price FROM products')
        rows = cursor.fetchall()
        conn.close()
        
        if not rows: return "📦 المخزن فارغ حالياً."
        
        output = "📋 قائمة منتجات SUHAIL ELUCE:\n"
        output += "---------------------------\n"
        for row in rows:
            output += f"🔹 {row[0]} -> السعر: {row[1]} ريال\n"
        return output
    
    return "💡 تم التحليل بنجاح."
