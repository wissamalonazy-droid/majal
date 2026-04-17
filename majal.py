import re

# ذاكرة المتغيرات
variables = {}

def tokenize(code):
    if not code: return []
    token_specification = [
        ('VAR',      r'عرف|VAR'),          
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
    return [(mo.lastgroup, mo.group()) for mo in re.finditer(tok_regex, code) if mo.lastgroup not in ['SKIP', 'NEWLINE']]

def run_interpreter(raw_code):
    global variables
    variables = {} # تصغير الذاكرة عند كل تشغيل
    results = []

    # إذا كان الكود يحتوي على HTML، نمرره فوراً للمعاينة
    if "<!DOCTYPE html>" in raw_code or "<html" in raw_code:
        return raw_code

    # معالجة المنطق البرمجي (مثل بايثون)
    try:
        tokens = tokenize(raw_code)
        i = 0
        while i < len(tokens):
            kind, value = tokens[i]
            
            if kind == 'VAR':
                var_name = tokens[i+1][1]
                if tokens[i+2][0] == 'ASSIGN':
                    variables[var_name] = tokens[i+3][1].strip('"')
                    results.append(f"💠 [مَجال]: تم حفظ '{var_name}'")
                    i += 5
            elif kind == 'PRINT':
                target = tokens[i+1][1]
                val = variables.get(target, target.strip('"'))
                results.append(f"📟 [مخرج]: {val}")
                i += 3
            else:
                i += 1
        return "\n".join(results) if results else "✅ الكود سليم"
    except Exception as e:
        return f"❌ خطأ في النواة: تأكد من تركيب الأوامر."
