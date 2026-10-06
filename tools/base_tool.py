from typing import Optional
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field
# 定义入参Schema
class RecommendDishInput(BaseModel):
    restaurant_type: str = Field(description="餐厅类型，例如火锅、湘菜、日料")
    spicy_prefer: Optional[str] = Field(default="不辣", description="辣度偏好：不辣/微辣/特辣")

class DishRecommendTool(BaseTool):
    name: str = "recommend_dish"
    description: str = "根据餐厅类型和辣度推荐招牌菜"
    args_schema: type[BaseModel] = RecommendDishInput

    def _run(self, restaurant_type: str, spicy_prefer: str = "不辣") -> str:
        menu_map = {
            "火锅": {"不辣": "骨汤锅底+肥牛", "微辣": "鸳鸯锅+毛肚", "特辣": "红汤牛油锅+鸭肠"},
            "湘菜": {"不辣": "小炒黄牛肉(减辣)", "微辣": "剁椒鱼头", "特辣": "爆辣口味虾"}
        }
        dish = menu_map.get(restaurant_type, {}).get(spicy_prefer, "暂无推荐")
        return f"【{restaurant_type}】推荐菜品：{dish}"

# 实例化工具
recommend_tool = DishRecommendTool()

# 测试
print(recommend_tool.invoke({"restaurant_type": "湘菜", "spicy_prefer": "微辣"}))
