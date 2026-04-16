import re

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
    ]
    tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup != 'SKIP']

def run_interpreter(tokens):
    global variables
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
                op, threshold = stmt[2][0], float(stmt[3][1])
                message = stmt[5][1].strip('"')
                val = float(variables.get(var_name, 0))
                check = (val > threshold if op == 'GT' else val < threshold if op == 'LT' else val == threshold)
                if check: results.append(f"🎯 [قرار]: {message}")

            elif cmd == 'BUILD':
                sys_type = stmt[1][1].strip('"')
                name = str(variables.get("الاسم", "نظام مَجال")).strip('"')
                
                if sys_type == "متجر":
                    results.append(f"🏗️ [كود المتجر]:\n<title>{name}</title>\n<h1 class='text-blue-500 text-3xl font-bold'>{name}</h1>\n<div class='grid'> </div>\n---\nCREATE TABLE products (id INT, name TEXT, price FLOAT);")
                elif sys_type == "مستشفى":
                    results.append(f"🏥 [كود المستشفى]:\n<title>نظام {name}</title>\n<nav class='bg-blue-900 p-4 text-white'>لوحة تحكم {name}</nav>\n---\nCREATE TABLE patients (id INT, name TEXT, history TEXT);")
                elif sys_type == "بنك":
                    results.append(f"🏦 [كود البنك]:\n<section class='p-10 bg-slate-900'>\n<h2 class='text-white'>بوابة {name} الآمنة</h2>\n</section>\n---\nCREATE TABLE accounts (acc_id INT, balance DECIMAL);")
                else:
                    results.append(f"🚀 [نظام مخصص]: جاري توليد كود لـ {sys_type}...")

            elif cmd == 'VAR':
                variables[stmt[1][1]] = stmt[3][1]

            elif cmd == 'PRINT':
                target = stmt[1][1]
                results.append(str(variables.get(target, target)).strip('"'))

        except: continue
    
    return "\n".join(results) if results else "✅ تم تنفيذ العمليات"
