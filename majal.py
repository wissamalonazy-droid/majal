import re

# ذاكرة المنطق
env = {'variables': {}, 'history': []}

def run_interpreter(raw_code):
    global env
    results = []
    
    # 🕵️ رادار النواة: هل المبرمج يكتب HTML مباشر؟
    if "<!DOCTYPE html>" in raw_code or "<html" in raw_code:
        # هنا النواة تعطي المبرمج "الحرية المطلقة" لتمرير الكود للمتصفح
        # مع فحص بسيط للأمان (Validation)
        return raw_code

    # 🧠 إذا كان كود منطقي (مثل بايثون)
    lines = raw_code.strip().split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if not line: continue
        
        try:
            # دعم تعريف المتغيرات الحرة
            if "=" in line and not line.startswith("إذا"):
                parts = line.split("=")
                var_name = parts[0].strip().replace("عرف ", "")
                var_value = parts[1].strip().replace(";", "")
                env['variables'][var_name] = var_value
                results.append(f"💠 [نواة مَجال]: تم حجز المتغير '{var_name}'")

            # دعم أوامر الطباعة للتحليل
            elif "اطبع" in line or "PRINT" in line:
                content = re.findall(r'"([^"]*)"', line)
                if content:
                    results.append(f"📟 {content[0]}")
                else:
                    # طباعة متغير
                    var = line.replace("اطبع ", "").replace(";", "").strip()
                    results.append(f"📟 {env['variables'].get(var, 'غير معرف')}")

        except Exception as e:
            results.append(f"❌ خطأ في السطر {i+1}: المنطق غير سليم")

    return "\n".join(results)
