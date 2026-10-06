import os
from dotenv import load_dotenv
from typing import Optional
from langchain_core.tools import tool, StructuredTool, BaseTool, convert_runnable_to_tool
from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

# 加载本地环境变量
load_dotenv()

#  工具1：@tool 基础装饰器
@tool
def get_restaurant_avg_price(restaurant_name: str) -> str:
    """查询餐厅人均消费。
    Args:
        restaurant_name: 餐厅名字
    """
    mock_data = {"潮汕牛肉火锅": "人均 95元", "日料小馆": "人均 180元", "湘菜馆": "人均 75元"}
    price = mock_data.get(restaurant_name, "暂无该餐厅价格数据")
    return f"【{restaurant_name}】{price}"

#  工具2：@tool + parse_docstring
@tool(parse_docstring=True)
def calc_food_calorie(dish_name: str, weight_g: Optional[int] = 100) -> str:
    """估算菜品卡路里。

    Args:
        dish_name: 菜品名称，例如红烧肉、白米饭
        weight_g: 食物重量，单位克，默认100克
    """
    calorie_map = {"红烧肉": 395, "白米饭": 116, "炒青菜": 45}
    per_100g = calorie_map.get(dish_name, 100)
    total = per_100g * weight_g / 100
    return f"{dish_name} {weight_g}g 总热量：{total:.1f} 千卡"

#  工具3：StructuredTool
def split_aa_bill(total_money: float, person_count: int, tip: float = 0) -> str:
    """多人AA分摊账单，包含小费。
    Args:
        total_money: 总账单金额
        person_count: 聚餐人数
        tip: 小费金额，默认0
    """
    total = total_money + tip
    per_person = total / person_count
    return f"总账单{total}元，{person_count}人AA，每人应付：{per_person:.2f}元"

aa_tool = StructuredTool.from_function(split_aa_bill)

#  工具4：继承 BaseTool
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

recommend_tool = DishRecommendTool()

#  工具5：Runnable 转 Tool
class ReviewInput(BaseModel):
    review_text: str = Field(description="用户的餐厅点评文本")

review_runnable = RunnableLambda(lambda x: f"【点评摘要】{x['review_text'].split('。')[0]}")
review_summary_tool = convert_runnable_to_tool(
    review_runnable,
    name="review_summary",
    description="提取用户点评核心摘要",
    args_schema=ReviewInput,
)

#  Agent 组装与运行
if __name__ == "__main__":
    # 初始化大模型
    llm = ChatOpenAI(
        model=os.getenv('DASHSCOPE_MODEL'),
        api_key=os.getenv("DASHSCOPE_API_KEY"),
        base_url=os.getenv('DASHSCOPE_BASE_URL')
    )

    # 注册全部工具
    tools = [get_restaurant_avg_price, calc_food_calorie, aa_tool, recommend_tool, review_summary_tool]

    # 创建新版Agent
    agent = create_agent(
        model=llm,
        tools=tools,
        system_prompt="你是美食探店助手，可调用对应工具完成用户需求，整合工具结果给出完整、清晰的回答。"
    )

    # 测试对话
    user_query = "周末4个人去湘菜馆，总消费500元，加50元小费，推荐微辣菜品并计算AA账单，同时帮我摘要这条点评：这家店牛肉很嫩，上菜速度快。但是排队太久，周末建议提前预约。"
    result = agent.invoke({"messages": [("human", user_query)]})

    print("n==== 最终回答 ====")
    print(result["messages"][-1].content)
