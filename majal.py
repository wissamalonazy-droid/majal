import re

variables = {}

def tokenize(code):
    if not code: return []
    token_specification = [
        ('VAR',      r'عرف'),          
        ('BUILD',    r'ابني'),         
        ('ID',       r'[A-Za-z_أ-ي][A-Za-z0-9_أ-ي]*'), 
        ('NUMBER',   r'\d+(\.\d+)?'),  
        ('STRING',   r'"[^"]*"'),      
        ('ASSIGN',   r'='),            
        ('END',      r';'),            
        ('SKIP',     r'[ \t]+'),       
        ('NEWLINE',  r'\n'),           
    ]
    tokens = []
    line = 1
    for mo in re.finditer('|'.join('(?P<%s>%s)' % pair for pair in token_specification), code):
        kind = mo.lastgroup
        value = mo.group()
        if kind == 'NEWLINE': line += 1
        elif kind == 'SKIP': continue
        else: tokens.append((kind, value, line))
    return tokens

def run_interpreter(tokens, raw_code):
    global variables
    variables = {} # تصقير الذاكرة لكل عملية بناء جديدة
    errors = []
    
    # 🕵️ فحص الفواصل المنقوطة قبل كل شيء
    raw_lines = raw_code.strip().split('\n')
    for i, l in enumerate(raw_lines):
        if l.strip() and not l.strip().endswith(';'):
            errors.append(f"⚠️ السطر {i+1}: نسيت تحط ';' في نهاية الأمر.")

    statements = []
    current_stmt = []
    for t in tokens:
        current_stmt.append(t)
        if t[0] == 'END':
            statements.append(current_stmt)
            current_stmt = []

    # إذا فيه أخطاء هيكلية نوقف فوراً
    if errors:
        return "❌ [أخطاء برمجية في كود مَجال]:\n" + "\n".join(errors)

    output_html = ""
    for stmt in statements:
        try:
            cmd = stmt[0][0]
            if cmd == 'VAR':
                # فحص تركيب جملة التعريف: عرف + اسم + = + قيمة + ;
                if len(stmt) < 5 or stmt[2][0] != 'ASSIGN':
                    errors.append(f"❌ السطر {stmt[0][2]}: تركيب أمر 'عرف' غلط. (تأكد من وجود '=')")
                else:
                    variables[stmt[1][1]] = stmt[3][1].strip('"')
            
            elif cmd == 'BUILD':
                # تنفيذ البناء فقط إذا كانت البيانات مكتملة
                name = variables.get("الاسم", "متجر غير مسمى")
                color = variables.get("اللون", "#3b82f6")
                # هنا يتم استدعاء قالب البناء المطور (HTML)
                output_html = f"" 
            else:
                errors.append(f"❓ السطر {stmt[0][2]}: الأمر '{stmt[0][1]}' غير مفهوم في لغة مَجال.")
        except:
            errors.append(f"❌ السطر {stmt[0][2]}: فيه مشكلة في كتابة السطر.")

    if errors:
        return "⚠️ [تقرير الأخطاء]:\n" + "\n".join(errors)
    
    return "✅ الكود سليم 100%! المبرمج وسام حر في بناء إمبراطوريته."
