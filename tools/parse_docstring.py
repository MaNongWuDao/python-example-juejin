from typing import Optional
from langchain_core.tools import tool

@tool(parse_docstring=True)
def calc_food_calorie(dish_name: str, weight_g: Optional[int] = 100) -> str:
    """估算菜品卡路里。
    
    Args:
        dish_name: 菜品名称，例如红烧肉、白米饭
        weight_g: 食物重量，单位克，默认100克
    """
    calorie_map = {
        "红烧肉": 395,
        "白米饭": 116,
        "炒青菜": 45
    }
    per_100g = calorie_map.get(dish_name, 100)
    total = per_100g * weight_g / 100
    return f"{dish_name} {weight_g}g 总热量：{total:.1f} 千卡"

# 测试
print(calc_food_calorie.invoke({"dish_name": "红烧肉", "weight_g": 200}))
