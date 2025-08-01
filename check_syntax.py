"""
فحص صحة بناء الجملة للملفات
"""
import ast
import sys
from pathlib import Path

def check_file_syntax(file_path):
    """فحص صحة بناء الجملة لملف Python"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # محاولة تحليل الكود
        ast.parse(content)
        return True, None
    except SyntaxError as e:
        return False, f"خطأ في بناء الجملة: {e}"
    except Exception as e:
        return False, f"خطأ: {e}"

def main():
    """فحص جميع ملفات Python"""
    files_to_check = [
        'main.py',
        'download.py', 
        'utils.py',
        'test_bot.py',
        'health_check.py',
        'setup.py',
        'simple_example.py'
    ]
    
    print("🔍 فحص صحة بناء الجملة...")
    print("=" * 40)
    
    all_good = True
    
    for file_name in files_to_check:
        if Path(file_name).exists():
            is_valid, error = check_file_syntax(file_name)
            if is_valid:
                print(f"✅ {file_name}")
            else:
                print(f"❌ {file_name}: {error}")
                all_good = False
        else:
            print(f"⚠️ {file_name}: الملف غير موجود")
    
    print("=" * 40)
    if all_good:
        print("🎉 جميع الملفات صحيحة!")
    else:
        print("🔧 يرجى إصلاح الأخطاء المذكورة أعلاه")
    
    return all_good

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)