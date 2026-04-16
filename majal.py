import re

# ذاكرة اللغة
variables = {}

def tokenize(code):
    token_specification = [
        ('IF',       r'إذا'),          
        ('BUILD',    r'ابني'),         
        ('VAR',      r'عرف'),          
        ('PRINT',    r'اطبع'),         
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'),  
        ('STRING',   r'"[^"]*"'),      
        ('ASSIGN',   r'='),            
        ('GT',       r'>'),            
        ('LT',       r'<'),            
        ('EQ',       r'=='),           
        ('END',      r';'),            
        ('SKIP',     r'[ \t]+'),       
        ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    # الفلترة هنا صارت أقوى عشان ما يضرب الكود مع الرموز
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "⚠️ المحرك بانتظار أوامرك..."
    
    results = []
    statements = []
    current_stmt = []
    
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    for stmt in statements:
        try:
            cmd = stmt[0][0]

            if cmd == 'IF':
                var_name = stmt[1][1]
                op = stmt[2][0]
                threshold = float(stmt[3][1])
                # تأكد من وجود أمر بعد الشرط
                action = stmt[4][0]
                message = stmt[5][1].strip('"')
                
                val = float(variables.get(var_name, 0))
                check = (val > threshold if op == 'GT' else val < threshold if op == 'LT' else val == threshold)

                if check:
                    results.append(f"🎯 [منطق]: {message}")
                else:
                    results.append(f"⚪ [منطق]: لم يتحقق الشرط.")

            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "نظام مَجال")).strip('"')
                currency = str(variables.get("العملة", "SAR")).strip('"')

                if sys_type == "متجر":
                    results.append(f"🏗️ [بناء]: تم إنشاء متجر {name} ({currency})")
                elif sys_type == "مستشفى":
                    results.append(f"🏥 [بناء]: تم إنشاء هيكل (مستشفى) لـ {name}")
                elif sys_type == "بنك":
                    results.append(f"🏦 [بناء]: تم هندسة نظام {name} البنكي")
                else:
                    results.append(f"📦 [بناء]: تم بناء نظام {sys_type} مخصص")

            elif cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]
                results.append(f"✅ تم حفظ [{stmt[1][1]}]")

            elif cmd == 'PRINT':
                target = stmt[1][1]
                results.append(str(variables.get(target, target)).strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ في السطر: تأكد من صياغة الأمر")
    
    return "\n".join(results)
