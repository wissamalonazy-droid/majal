import re

# ذاكرة النواة المركزية (تخزين المتغيرات والدوال)
env = {
    'variables': {},
    'functions': {}
}

def tokenize(code):
    if not code: return []
    # تعريف القواعد البرمجية الشاملة
    token_specification = [
        ('IF',       r'إذا|IF'),          # الشروط
        ('ELSE',     r'وإلا|ELSE'),       # البدائل
        ('LOOP',     r'كرر|FOR|WHILE'),   # الحلقات والتكرار
        ('FUNC',     r'مهمة|DEF'),        # الدوال (المهمات)
        ('VAR',      r'عرف|VAR'),         # تعريف المتغيرات
        ('PRINT',    r'اطبع|PRINT'),       # المخرجات (Console)
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'),     
        ('STRING',   r'"[^"]*"'),         
        ('ASSIGN',   r'='),               
        ('OP',       r'[+\-*/><!=]+'),    # العمليات الحسابية والمنطقية
        ('END',      r';'),               
        ('LBRACE',   r'\{'),              # بداية بلوك برمجي
        ('RBRACE',   r'\}'),              # نهاية بلوك برمجي
        ('SKIP',     r'[ \t]+'),          
        ('NEWLINE',  r'\n'),              
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(raw_code):
    global env
    env['variables'] = {} # تصفير الذاكرة في كل تشغيل جديد
    results = []

    # 1. فحص الهوية: إذا كان الكود واجهة رسومية (HTML) مرره فوراً
    if any(tag in raw_code.lower() for tag in ["<!doctype html>", "<html", "<body", "<div", "<style"]):
        return raw_code

    # 2. معالجة المنطق البرمجي (المترجم الذكي)
    try:
        tokens = tokenize(raw_code)
        i = 0
        while i < len(tokens):
            kind, value = tokens[i]

            # --- نظام المتغيرات والحساب (القوة الرياضية) ---
            if kind == 'VAR':
                var_name = tokens[i+1][1]
                if tokens[i+2][0] == 'ASSIGN':
                    expr = ""
                    j = i + 3
                    while j < len(tokens) and tokens[j][0] != 'END':
                        t_val = tokens[j][1]
                        # استبدال المتغيرات المخزنة بقيمها داخل المعادلات
                        if tokens[j][0] == 'ID' and t_val in env['variables']:
                            t_val = str(env['variables'][t_val])
                        expr += t_val
                        j += 1
                    
                    try:
                        # تنفيذ العملية الحسابية/المنطقية
                        env['variables'][var_name] = eval(expr.replace('"', ''))
                        results.append(f"💠 [مَجال]: {var_name} = {env['variables'][var_name]}")
                    except:
                        # تعيين كنص إذا لم تكن عملية حسابية
                        env['variables'][var_name] = expr.strip('"')
                        results.append(f"💠 [مَجال]: تم حفظ '{var_name}'")
                    i = j + 1

            # --- نظام المخرجات (اطبع) ---
            elif kind == 'PRINT':
                target = tokens[i+1][1]
                val = env['variables'].get(target, target.strip('"'))
                results.append(f"📟 [مخرج]: {val}")
                i += 3

            # --- نظام الشروط (إذا) ---
            elif kind == 'IF':
                condition_expr = tokens[i+1][1]
                # معالجة المتغيرات داخل الشرط
                for v_name, v_val in env['variables'].items():
                    condition_expr = condition_expr.replace(v_name, str(v_val))
                
                if eval(condition_expr):
                    results.append("🔍 [نظام مَجال]: الشرط تحقق ✅")
                else:
                    results.append("🔍 [نظام مَجال]: الشرط لم يتحقق ❌")
                i += 2

            # --- نظام التكرار (كرر) ---
            elif kind == 'LOOP':
                try:
                    times = int(tokens[i+1][1])
                    results.append(f"🔄 [تكرار]: تنفيذ المهمة {times} مرات..")
                    # (يمكن تطوير هذا الجزء لتكرار أوامر فعلية لاحقاً)
                except:
                    results.append("⚠️ خطأ: يجب تحديد عدد مرات التكرار برقم")
                i += 2

            # --- نظام الدوال (مهمة) ---
            elif kind == 'FUNC':
                func_name = tokens[i+1][1]
                results.append(f"🛠️ [نظام مَجال]: تم تسجيل المهمة البرمجية '{func_name}'")
                i += 3

            else:
                i += 1

        return "\n".join(results) if results else "✅ الكود سليم (لا يوجد مخرجات)"
    
    except Exception as e:
        return f"❌ خطأ منطقي: تأكد من صياغة الأوامر (نسيت فاصلة منقوطة ; أو قوس؟)"
