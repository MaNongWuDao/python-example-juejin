
from langchain_core.tools import  StructuredTool
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

# 封装成StructuredTool
aa_tool = StructuredTool.from_function(split_aa_bill)

# 测试
print(aa_tool.invoke({"total_money": 500, "person_count": 4, "tip": 50}))
