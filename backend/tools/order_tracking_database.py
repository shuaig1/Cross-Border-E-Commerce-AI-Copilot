from langchain.tools import tool
from backend.data.data_manager import db

@tool
def lookup_order(order_id:str)->str:
    """查询订单状态"""
    order = db.get_order(order_id)
    if not order:
        return f"未找到该订单{order_id},请核实订单号"
    return (
        f"订单号:{order['order_id']}\n"
        f"商品:{order['items']} \n"
        f"金额:{order['total']}\n"
        f"订单状态:{order['status']}\n"
        f"物流单号:{order['tracking'] or '暂无'}({order['carrier']})\n"
        f"预计送达日期:{order['eta']}\n"
    )

@tool
def lookup_logistics(tracking_number:str)->str:
    """查询物流轨迹"""
    log = db.get_logistics(tracking_number)
    if not log:
        return f"暂无物流单号{tracking_number}的轨迹信息"
    return (
        f"物流单号:{tracking_number}\n"
        f"当前状态:{log['status']}\n"
        f"最新位置:{log['location']}\n"
        f"时间:{log['timestamp']}\n"
    )