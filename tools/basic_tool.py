
from langchain_core.tools import tool

@tool
def get_restaurant_avg_price(restaurant_name: str) -> str:
    """查询餐厅人均消费。
    Args:
        restaurant_name: 餐厅名字
    """
    # 模拟数据库查询
    mock_data = {
        "潮汕牛肉火锅": "人均 95元",
        "日料小馆": "人均 180元",
        "湘菜馆": "人均 75元"
    }
    price = mock_data.get(restaurant_name, "暂无该餐厅价格数据")
    return f"【{restaurant_name}】{price}"

# 测试
print(get_restaurant_avg_price.invoke({"restaurant_name": "潮汕牛肉火锅"}))
