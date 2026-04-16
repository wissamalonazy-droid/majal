import re

# ذاكرة اللغة لتخزين المتغيرات
variables = {}

def tokenize(code):
    token_specification = [
        ('IF',       r'إذا'),          # أمر الشرط الجديد
        ('BUILD',    r'ابني'),         
        ('VAR',      r'عرف'),          
        ('PRINT',    r'اطبع'),         
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'),  
        ('STRING',   r'"[^"]*"'),      
        ('ASSIGN',   r'='),            
        ('GT',       r'>'),            # أكبر من
        ('LT',       r'<'),            # أصغر من
        ('EQ',       r'=='),           # يساوي
        ('END',      r';'),            
        ('SKIP',     r'[ \t]+'),       
        ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(tokens):
    global variables
    if not tokens: return "⚠️ محرك مَجال 2.0.1 جاهز للعمل..."
    
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

            # 1️⃣ المنطق الشرطي (القرار الذكي)
            if cmd == 'IF':
                # هيكل الأمر: إذا [متغير] [علامة] [رقم] [أمر] [نص] ;
                var_name = stmt[1][1]
                op = stmt[2][0]
                threshold = float(stmt[3][1])
                action = stmt[4][0] # PRINT
                message = stmt[5][1].strip('"')

                val = float(variables.get(var_name, 0))
                
                check = False
                if op == 'GT': check = val > threshold
                elif op == 'LT': check = val < threshold
                elif op == 'EQ': check = val == threshold

                if check:
                    results.append(f"🎯 [منطق مَجال]: تحقق الشرط -> {message}")
                else:
                    results.append(f"⚪ [منطق مَجال]: لم يتحقق الشرط.")

            # 2️⃣ نظام البناء الشامل
            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "نظام مَجال")).strip('"')
                currency = str(variables.get("العملة", "SAR")).strip('"')

                if sys_type == "متجر":
                    results.append(f"🏗️ [بناء]: تم توليد كود متجر ({name}) بالعملة ({currency}) جاهز للنسخ.")
                elif sys_type == "بنك":
                    results.append(f"🏦 [بناء]: تم هندسة النظام البنكي لـ ({name}) بأعلى معايير الأمان.")
                else:
                    results.append(f"📦 [بناء]: تم إنشاء هيكل ({sys_type}) مخصص.")

            # 3️⃣ تعريف المتغيرات والطباعة
            elif cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]
                results.append(f"✅ تم حفظ [{stmt[1][1]}]")

            elif cmd == 'PRINT':
                target = stmt[1][1]
                results.append(str(variables.get(target, target)).strip('"'))

        except Exception as e:
            results.append(f"❌ خطأ منطقي: {str(e)}")
    
    return "\n".join(results)
