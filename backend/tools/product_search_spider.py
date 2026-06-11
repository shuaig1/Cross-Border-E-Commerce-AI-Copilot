#暂时没有商品数据用于爬取其他店铺商品
from langchain.tools import tool
import requests
from backend.config import Config

# 模拟浏览器的请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
    "Accept": "application/json, text/plain, */*",
}
@ tool
def search_products_online(query:str)->str:
    """
    在主流跨境店铺中实时搜索商品信息，输入商品关键词
    """
    query_lower = query.lower()

    #从配置中读取店铺策略
    target_url = None
    for store_name,keywords in Config.STORE_KEYWORDS.items():
        #已经有的店铺信息和输入的信息有一个关键字匹配就行
        if any(kw in query_lower for kw in keywords):
            target_url = Config.TARGET_STORES[store_name]
            break
    if target_url is None:
        target_url = Config.TARGET_STORES[Config.DEFAULT_STORE]

    try:
        response = requests.get(target_url,timeout=10,headers=HEADERS)
        response.raise_for_status()
        products = response.json().get('product',[])
        result =[]
        for product in products:
            if query_lower in product['title'].lower():
                variants = product.get('variants',[])
                price =f"${variants[0]['price']}" if variants and 'price' in variants[0] else "N/A"
                product_url =f"https://{target_url.split('/')[2]}/products/{product.get('handle','')}"
                result.append(f"{product['title']} - {price} - {product_url}")
                if len(result)>=3:
                    break
        if result:
            return "\n".join(result)
        else:
            return f"未找到与'{query}'强相关的商品，建议扩大搜索或联系人工。"
    except Exception as e:
        return f"实时商品查询暂时不可用({str(e)}),请稍后再试。"