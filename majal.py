import re

variables = {}

def tokenize(code):
    if not code: return []
    # تعريف الأوامر باللغتين (العربية والإنجليزية)
    token_specification = [
        ('VAR',      r'عرف|VAR'),          
        ('BUILD',    r'ابني|BUILD'),        
        ('PRINT',    r'اطبع|PRINT'),        
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'),  
        ('STRING',   r'"[^"]*"'),      
        ('ASSIGN',   r'='),            
        ('END',      r';'),            
        ('SKIP',     r'[ \t]+'),       
        ('NEWLINE',  r'\n'),           
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    tokens = []
    line_num = 1
    for mo in re.finditer(tok_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE': line_num += 1
        elif kind == 'SKIP': continue
        else: tokens.append((kind, value, line_num))
    return tokens

def run_interpreter(tokens, raw_code):
    global variables
    variables = {}
    results = []
    errors = []
    
    # تقسيم الجمل البرمجية
    statements = []
    current_stmt = []
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    # 🕵️ فحص هيكلي عالمي (الأخطاء تظهر بلغة المبرمج)
    raw_lines = raw_code.strip().split('\n')
    for i, line in enumerate(raw_lines):
        if line.strip() and not line.strip().endswith(';'):
            errors.append(f"⚠️ Line {i+1}: Missing ';' at the end of statement.")

    if errors: return "❌ [Compiler Error]:\n" + "\n".join(errors)

    # تنفيذ المنطق البرمجي (عربي + إنجليزي)
    for stmt in statements:
        try:
            cmd = stmt[0][0]
            
            if cmd == 'VAR':
                var_name = stmt[1][1]
                var_value = stmt[3][1].strip('"')
                variables[var_name] = var_value
            
            elif cmd == 'PRINT':
                val = variables.get(stmt[1][1], stmt[1][1].strip('"'))
                results.append(f"Console: {val}")

            elif cmd == 'BUILD':
                # بناء الموقع يدعم اللغتين بناءً على محتوى المتغيرات
                name = variables.get("Name", variables.get("الاسم", "Global Store"))
                color = variables.get("Color", variables.get("اللون", "#3b82f6"))
                lang = "en" if "Name" in variables else "ar"
                dir_attr = "ltr" if lang == "en" else "rtl"
                
                # هنا يولد المحرك كود HTML ذكي يتكيف مع اللغة المختارة
                results.append(f"🏗️ Building {lang.upper()} Website: {name}...")
                # (سيتم حقن قالب الـ HTML العالمي هنا)

        except Exception:
            errors.append(f"❌ Syntax Error on line {stmt[0][2]}")

    if errors: return "⚠️ [Error Report]:\n" + "\n".join(errors)
    return "\n".join(results)
