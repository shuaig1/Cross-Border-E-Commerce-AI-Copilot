from langchain.tools import tool
import json
import os
from backend.data.data_manager import db

import jieba
from backend.data import vector_store
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
    if vector_store.collection.count()==0:
        return "商品向量数据库为空。请先导入数据"

    #语义检索top 3
    results =vector_store.collection.query(
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
    product_count = len(vector_store.bm25_product_list)
    for rank,doc_id in enumerate(vector_results["ids"][0]):
        idx = int(doc_id.replace("prod_",""))
        if idx < 0 or idx >= product_count:
            continue
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

def _hybrid_search(query:str,vector_top_n:int= 10,bm25_top_n:int = 10,final_top_n:int = 3,threshold:float = 1.5):
    """
    混合检索:向量检索+bm25关键字检索->RRF融合->相似度阈值过滤
    返回:(formatted_items,item_data_list)
         formatted_items:[(title,price,url,description),...]
    """
    #1.向量检索(召回更多候选)
    vector_results = vector_store.collection.query(
        query_texts=[query],
        n_results=min(vector_top_n, vector_store.collection.count()),
        include=["documents","metadatas","distances"],
    )
    #2.BM25关键字检索
    bm25_doc_indices =[]
    bm25_scores =[]
    if vector_store.bm25_index is not None:
        tokenized_query = list(jieba.cut(query))
        scores = vector_store.bm25_index.get_scores(tokenized_query)
        #按分数降序取top N
        indexed_scores = [(i,scores[i]) for i in range(len(scores))]
        indexed_scores.sort(key=lambda x:x[1],reverse=True)
        top_bm25 =indexed_scores[:bm25_top_n]
        bm25_doc_indices = [i for i, _ in top_bm25]
        bm25_scores = scores
    else:
        #BM25不可用时降级为纯向量检索
        top_indices =[]
        for doc_id in vector_results["ids"][0]:
            idx =int(doc_id.replace("prod_",""))
            top_indices.append(idx)
        items=[]
        for idx in top_indices[:final_top_n]:
            if idx < 0 or idx >= len(vector_store.bm25_product_list):
                continue
            product =vector_store.bm25_product_list[idx]
            items.append((
                product["title"],
                product.get("price","N/A"),
                product.get("url",""),
                product.get("description","")
            ))
        return items
    #3.RRF融合
    ranked = _rrf_fusion(vector_results,bm25_scores,bm25_doc_indices,k=60,top_n=final_top_n)
    #4.相似度阈值过滤+组装结果
    items= []
    vector_doc_ids = vector_results["ids"][0]
    vector_distances = vector_results["distances"][0]

    for idx,rrf_score in ranked:
        #查找该商品在向量检索中的distance
        doc_id = f"prod_{idx}"
        distance =None
        if doc_id in vector_doc_ids:
            pos = vector_doc_ids.index(doc_id)
            distance = vector_distances[pos]
        
        #相似度阈值过滤:只在向量检索命中时检查，BM25单独命中的保留
        if distance is not None and distance >= threshold:
            continue

        if idx < 0 or idx >= len(vector_store.bm25_product_list):
            continue
        product =vector_store.bm25_product_list[idx]
        items.append((
            product["title"],
            product.get("price","N/A"),
            product.get("url",""),
            product.get("description","")
        ))
    return items

@tool
def search_products_local_hybrid(query:str)->str:
    """
    混合搜索商品信息(关键词精确匹配+语义相似度搜索)。
    输入用户查询，先用BM25匹配关键词，再结合向量语义搜索，综合排序后返回最相关的商品
    返回商品名称、价格、描述和链接。
    """
    if vector_store.collection.count()==0:
        return "商品向量数据库为空。请先导入数据。"

    items = _hybrid_search(query)

    if not items:
        return f"没有找到与'{query}'相关的商品,请尝试其他关键词。"
    
    result_parts = []
    for title,price,url,description in items:
        result_parts.append(f"【{title}】${price}\n{description}\n->{url}")

    return "\n\n".join(result_parts)
    
