from langchain.tools import tool
import json
import os
from backend.data.data_manager import db

import jieba
from backend.data.vector_store import collection,bm25_index,bm25_product_list
#动态获取product,json 路径
DATA_DIR =os.path.join(os.path.dirname(__file__),"..","data")

PRODUCTS_FILE = os.path.join(DATA_DIR,"product_search.json")
# print("DATA_DIR:",DATA_DIR)
# print("PRODUCTS_FILE:",PRODUCTS_FILE)
# print(os.path.abspath(PRODUCTS_FILE))
def _load_products():
    """从本地JSON文件加载商品列表"""
    try:
        with open(PRODUCTS_FILE,"r",encoding="utf-8") as f:
            return  json.load(f)
    except FileNotFoundError:
        return  []
    except json.JSONDecodeError:
        return []

@tool
def search_products_local_Json(query:str)->str:
    """
    从本地商品json库中搜索商品信息。
    输入商品关键词(如"运动"、"瑜伽"、"耳机"),
    返回匹配的商品名称、价格、描述和链接。
    """
    query_lower = query.lower()
    products = _load_products()
    # products = db.search_products(query_lower)

    if not products:
        return "商品Json库暂不可用，请稍后重试或联系人工客服"

    results = []
    for product in products:
        title = product.get('title','')
        desc = product.get('description','')
        if query_lower in title.lower() or query_lower in desc.lower():
            price =product.get('price','N/A')
            url = product.get('url','#')
            results.append(f"【{title}】$ {price}\n{desc}\n👉{url}")
            if len(results)>=3:
                break
    if results:
        return "\n\n".join(results)
    else:
        return f"未找到与'{query}'强相关的商品，建议扩大搜索或联系人工"

@ tool
def search_products_local_database(query:str)->str:
    """
    从本地商品数据库中搜索商品信息。
    输入商品关键词(如"运动"、"瑜伽"、"耳机"),
    返回匹配的商品名称、价格、描述和链接。
    """
    products = db.search_products(query)
    if not products:
        return "商品数据库暂不可用，请稍后重试或联系人工客服"

    results = []
    for p in products:
        price =p.get("price","N/A")
        desc = p.get("description","")
        results.append(f"【{p['title']}】${price}\n {desc}")

    return "\n\n".join(results)

@tool()
def search_products_local_vector_store(query:str)->str:
    """语义搜索商品信息，输入用户查询，返回最相关的产品"""
    if collection.count()==0:
        return "商品向量数据库为空。请先导入数据"

    #语义检索top 3
    results =collection.query(
        query_texts=[query],
        n_results=3
    )
    if not results["documents"][0]:
        return f"没有找到与'{query}'语义相似的商品,请尝试其他关键词。"

    #组织返回格式
    items =[]
    for doc,mata in zip(results["documents"][0],results["metadatas"][0]):
        price =mata.get("price","N/A")
        title = mata.get("title","未知商品")
        url = mata.get("url","")
        items.append(f"【{title}】${price}\n{doc}\n->{url}")
    return "\n\n".join(items)

def _rrf_fusion(vector_results,bm25_scores,bm25_doc_indices,k=60,top_n=3):
    #向量排名->RRF分数
    scores ={}
    for rank,doc_id in enumerate(vector_results["ids"][0]):
        idx = int(doc_id.replace("prod_",""))
        scores[idx] = scores.get(idx,0)+1.0/(k+rank+1)

    #BM25按分数排序->排名->RRF分数
    ranked_bm25 = sorted(
        [(i,bm25_scores[i]) for i in bm25_doc_indices],
        key=lambda x:x[1],reverse=True
    )
    for rank,(idx,_) in enumerate(ranked_bm25):
        scores[idx] = scores.get(idx,0)+1.0/(k+rank+1)

    ranked = sorted(scores.items(),key=lambda x:x[1],reverse=True)
    return ranked[:top_n]