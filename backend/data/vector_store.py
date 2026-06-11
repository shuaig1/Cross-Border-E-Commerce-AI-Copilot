import os
import json
from chromadb import PersistentClient
from chromadb.utils import embedding_functions
from rank_bm25 import BM25Okapi
import jieba

#持久化目录
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "chroma_db")
#使用开源中文嵌入模型
embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="shibing624/text2vec-base-chinese"
)
client = PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection(
    name="products",
    embedding_function=embedding_fn,
)
bm25_index =None #BM250kapi实例
bm25_product_list = []#商品完整数据列表

def init_vector_store():
    """从product_vector_rag_store.json导入数据到Chroma"""
    #检查是否已导入
    # if collection.count() > 0:
    #     return

    products_path = os.path.join(os.path.dirname(__file__), "product_vector_rag_store.json")
    with open(products_path, "r", encoding="utf-8") as f:
        products = json.load(f)

    ids = []
    documents=[]
    metadatas = []

    for i,p in enumerate(products):
        ids.append(f"prod_{i}")
        #合并标题和描述作为嵌入文本

        documents.append(f"{p['title']}:{p['description']}")
        metadatas.append({
        "title":p["title"],
        "price":p["price"],
        "url":p.get("url","")
        })

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
    )
    #构建BM25关键词索引
    global bm25_index,bm25_product_list
    #用jieba对每个商品的文本做分词
    tokenized_docs = [list(jieba.cut(doc)) for doc in documents]
    bm25_index = BM25Okapi(tokenized_docs)
    bm25_product_list = products
    print(f"BM25索引已构建，共{len(tokenized_docs)}条")
    print(f"已导入{len(ids)}件商品到向量数据库")