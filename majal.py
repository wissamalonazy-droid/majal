import re

def run_interpreter(raw_code):
    # ذاكرة الجلسة
    env = {'vars': {}}
    results = []

    # 1. تمرير واجهات الـ HTML فوراً
    if any(tag in raw_code.lower() for tag in ["<!doctype html>", "<html", "<body", "<div"]):
        return raw_code

    # 2. تنظيف الكود ومعالجته سطر بسطر
    lines = raw_code.strip().split('\n')
    
    for line in lines:
        line = line.strip()
        if not line or line.startswith("//"): continue
        
        try:
            # --- نظام التعريف (عرف X = Y ;) ---
            if "عرف" in line and "=" in line:
                # تنظيف السطر من كلمة "عرف" والفاصلة المنقوطة
                clean_line = line.replace("عرف", "").replace(";", "").strip()
                parts = clean_line.split("=")
                var_name = parts[0].strip()
                expression = parts[1].strip()

                # استبدال المتغيرات المعروفة في المعادلة
                for v_name, v_val in env['vars'].items():
                    expression = expression.replace(v_name, str(v_val))
                
                try:
                    # محاولة حساب القيمة إذا كانت رياضية
                    env['vars'][var_name] = eval(expression)
                    results.append(f"💠 [مَجال]: تم حفظ {var_name} بقيمة {env['vars'][var_name]}")
                except:
                    # حفظ كقيمة نصية إذا فشل الحساب
                    env['vars'][var_name] = expression.strip('"')
                    results.append(f"💠 [مَجال]: تم حفظ النص في {var_name}")

            # --- نظام المخرجات (اطبع X ;) ---
            elif "اطبع" in line:
                content = line.replace("اطبع", "").replace(";", "").strip()
                val = env['vars'].get(content, content.strip('"'))
                results.append(f"📟 [مخرج]: {val}")

            # --- نظام الشروط المبسط (إذا X > Y) ---
            elif "إذا" in line:
                cond = line.replace("إذا", "").strip()
                # معالجة المتغيرات في الشرط
                for v_name, v_val in env['vars'].items():
                    cond = cond.replace(v_name, str(v_val))
                
                if eval(cond):
                    results.append("🔍 [نظام مَجال]: الشرط تحقق ✅")
                else:
                    results.append("🔍 [نظام مَجال]: الشرط لم يتحقق ❌")

        except Exception as e:
            results.append(f"⚠️ خطأ في السطر: {line}")

    return "\n".join(results) if results else "📝 اكتب كودك بوضوح..."
