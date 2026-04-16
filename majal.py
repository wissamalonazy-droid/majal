# --- جزء من تحديث run_interpreter للمرحلة الأولى ---

if stmt[0][0] == 'BUILD':
    system_type = stmt[1][1].strip('"')
    
    if system_type == "متجر":
        generated_logic = f"""
        📦 [نظام متجر مجال جاهز]:
        - تم إنشاء جدول: Products (المنتجات)
        - تم إنشاء جدول: Orders (الطلبات)
        - تم تفعيل معالج الدفع الذكي.
        """
        results.append(generated_logic)
        
    elif system_type == "مدرسة":
        generated_logic = f"""
        🏫 [نظام مدرسة مجال جاهز]:
        - تم إنشاء جدول: Students (الطلاب)
        - تم إنشاء جدول: Grades (الدرجات)
        - تم تفعيل نظام الغياب التلقائي.
        """
        results.append(generated_logic)
    else:
        results.append(f"🏗️ [بناء مجال]: جاري إنشاء نظام مخصص لـ {system_type}...")
