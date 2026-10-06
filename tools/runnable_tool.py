from langchain_core.runnables import RunnableLambda
from langchain_core.tools import convert_runnable_to_tool
from pydantic import BaseModel, Field

# 定义输入参数模型
class ReviewInput(BaseModel):
    review_text: str = Field(description="用户的餐厅点评文本")

# 原始Runnable：清洗点评文本，提取一句话摘要
review_runnable = RunnableLambda(lambda x: f"【点评摘要】{x['review_text'].split('。')[0]}")

# Runnable转Tool，修正参数名 args_schema
review_summary_tool = convert_runnable_to_tool(
    review_runnable,
    name="review_summary",
    description="提取用户点评第一句话摘要",
    args_schema=ReviewInput,  # 这里！！改成 args_schema，并且传入我们定义好的ReviewInput
)

# 测试调用
print(review_summary_tool.invoke({"review_text": "这家店牛肉很嫩，上菜速度快。但是排队太久，周末建议提前预约。"}))
