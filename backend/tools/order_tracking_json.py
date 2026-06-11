from langchain.tools import tool
import json
import os

ORDERS_FILE = os.path.join(os.path.dirname(__file__),"..","data","orders.json")
LOGISTICS_FILE = os.path.join(os.path.dirname(__file__),"..","data","logistics.json")

def _load_json(path):
    try:
        with open(path,"r",encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError):
        return []

@tool
def lookup_order(order_id:str)->str:
    """
    查询订单状态，输入订单号(如 ORD--20240501-001),返回订单详情、物流跟踪号及预计送达日期
    """
    orders = _load_json(ORDERS_FILE)
    for order in orders:
        if order.get("order_id")==order_id:
            item = ",".join(order.get("items",[]))
            status = order.get("status","未知")
            tracking = order.get("tracking","暂无")
            carrier = order.get("carrier","未知")
            eta = order.get("eta","未知")
            total = order.get("total","N/A")
            return (
                f"订单号:{order_id}\n"
                f"商品:{item}\n"
                f"金额:{total}\n"
                f"订单状态:{status}\n"
                f"物流单号:{tracking}{carrier}\n"
                f"预计送达日期:{eta}\n"
            )
    return f"未找到该订单{order_id},请核实订单号"
@tool
def lookup_logistics(tracking_number:str)->str:
    """
    查询物轨迹，输入物流单号,返回最新物流信息
    """
    logistics = _load_json(LOGISTICS_FILE)
    for log in logistics:
        if log.get("tracking")==tracking_number:
            return (
                f"物流单号:{tracking_number}\n"
                f"当前状态:{log.get('status')}\n"
                f"最新位置:{log.get('location')}\n"
                f"时间:{log.get('timestamp')}\n"
            )
    return f"暂无物流单号{tracking_number}的轨迹信息"