#!/usr/bin/env python3
"""
修复缺失模板的路由脚本
将所有缺失模板的游戏页面路由修改为使用通用模板
"""

import re

def fix_app_routes():
    """修复app.py中的路由，使用通用模板"""
    
    # 读取当前的app.py文件
    with open('app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 需要修复的路由模式
    missing_templates = [
        'sprunki-banana', 'sprunki-ketchup', 'sprunki-garnold', 'sprunki-grown-up',
        'sprunki-phase-1-7', 'sprunki-phase-19-update', 'sprunki-phase-6-definitive',
        'sprunki-phase-6-definitive-all-alive', 'sprunki-phase-6-definitive-remaster',
        'sprunki-phase-777-3-7', 'sprunki-pyramixed', 'sprunki-pyramixed-melophobia',
        'sprunki-pyramixed-regretful', 'sprunki-pyramixed-ultimate-deluxe',
        'sprunki-retake-but-human', 'sprunki-retake-new-human', 'sprunki-shatter',
        'sprunki-spfundi', 'sprunki-sploinkers', 'sprunki-sprunkr', 'sprunki-sprunksters',
        'sprunki-sprured', 'sprunki-spruted', 'sprunki-swap-retextured', 'sprunki-ultimate-deluxe',
        'sprunki-upin-ipin', 'sprunki-wenda-edition', 'sprunklings', 'sprunki-agents',
        'sprunki-banana-porridge', 'sprunki-brud-edition-finale', 'sprunki-chaotic-good',
        'sprunki-dx', 'sprunki-fiddlebops', 'incredibox-rainbow-animal', 'incredibox-irrelevant-reunion',
        'sprunka'
    ]
    
    for template_name in missing_templates:
        # 查找对应的路由函数
        pattern = rf"(@app\.route\('/{re.escape(template_name)}'\)\s*def\s+\w+\(\):\s*)(.*?)(return render_template\('{re.escape(template_name)}\.html',.*?\))"
        
        # 替换模板调用
        def replace_template(match):
            route_def = match.group(1)
            function_body = match.group(2)
            
            # 提取页面标题
            page_title = template_name.replace('-', ' ').replace('sprunki ', '').title()
            if 'sprunki' not in page_title.lower():
                page_title = f"Sprunki {page_title}"
            
            # 生成新的return语句
            new_return = f"""return render_template('game-template.html',
                         page_title='{page_title}',
                         page_slug='{template_name}',
                         faq_data=faq_data)"""
            
            return route_def + function_body + new_return
        
        content = re.sub(pattern, replace_template, content, flags=re.DOTALL)
    
    # 写回文件
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ 修复了 {len(missing_templates)} 个缺失模板的路由")

if __name__ == "__main__":
    fix_app_routes()
    print("🎉 路由修复完成！") 