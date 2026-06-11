import sqlite3
import os
from typing import List,Dict,Optional

DB_PATH =os.path.join(os.path.dirname(__file__),"ecom.db")

class DataManager:
    """统一数据管理，代替所有JSON文件"""
    def __init__(self):
        self.conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self._init_tables()

    def _init_tables(self):
        cursor = self.conn.cursor()
        #商品表
        cursor.execute("""
         CREATE TABLE IF NOT EXISTS
         product(
             id INTEGER PRIMARY KEY AUTOINCREMENT,
             title TEXT NOT NULL,
             price REAL NOT NULL,
             description TEXT,
             url TEXT
         
                )
            """)
        #订单表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id TEXT UNIQUE NOT NULL,
            status TEXT NOT NULL,
            items TEXT,
            total REAL,
            tracking TEXT,
            carrier TEXT,
            eta TEXT
        )
        """)
        #物流表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        logistics(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tracking TEXT  NOT NULL,
        status TEXT,
        location TEXT,
        timestamp TEXT
        )
        
        """)
        #对话历史
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS
        conversations(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        msg_role TEXT NOT NULL,
        content TEXT NOT NULL,
        intent TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.conn.commit()
        self._seed_data(cursor)
    def _seed_data(self,cursor):
        """初始化示例数据(兼容JSON数据)"""
        #检查数据是否已存在
        cursor.execute("SELECT COUNT(*) FROM product")
        if cursor.fetchone()[0]==0:
            #插入商品
            products = [
                ("运动短裤 Pro", 29.99, "透气速干面料，适合健身和跑步"),
                ("环保桉树跑鞋", 89.99, "桉树纤维鞋面，轻便透气"),
                ("高腰瑜伽紧身裤", 39.99, "无痕面料，高腰收腹设计"),
                ("澳洲羊毛保暖拖鞋", 49.99, "澳洲羊毛内衬，柔软保暖"),
                ("夏日碎花连衣裙", 59.99, "轻薄透气，收腰设计"),
                ("快充移动电源 20000mAh", 25.99, "支持PD快充"),
                ("主动降噪蓝牙耳机", 79.99, "主动降噪，续航40小时"),
                ("防摔硅胶手机壳", 12.99, "液态硅胶，防摔抗震"),
            ]
            cursor.executemany("INSERT INTO product(title,price,description) VALUES(?,?,?)",products)
            #插入订单
            orders =[
                ("ORD-20240501-001", "已发货", "运动短裤 Pro", 29.99, "LX20240501CN", "FedEx", "2024-05-10"),
                ("ORD-20240502-002", "处理中", "环保桉树跑鞋, 高腰瑜伽紧身裤", 129.98, None, "DHL", "2024-05-12"),
                ("ORD-20240503-003", "已签收", "主动降噪蓝牙耳机", 79.99, "LX20240503US", "USPS", "2024-05-08"),

            ]
            cursor.executemany("INSERT INTO orders(order_id,status,items,total,tracking,carrier,eta) VALUES(?,?,?,?,?,?,?)",orders)
            #插入物流
            logistics = [
                ("LX20240501CN", "已发货", "中国", "2024-05-05 10:00:00"),
                ("LX20240502US", "处理中", "美国", "2024-05-07 14:30:00"),
                ("LX20240503US", "已签收", "美国", "2024-05-08 16:00:00"),
                ("LX20240504CN", "运输中", "广州集散中心", "2024-05-06 14:30"),
                ("LX20240505US", "已签收", "纽约布鲁克林", "2024-05-08 09:15"),
            ]
            cursor.executemany("INSERT INTO logistics(tracking,status,location,timestamp) VALUES(?,?,?,?)",logistics)
            self.conn.commit()
    #===商品查询==
    def search_products(self,keyword:str)->List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT title, price, description, url FROM product WHERE title LIKE ? OR description LIKE ? LIMIT 3",
            (f"%{keyword}%", f"%{keyword}%")
        )
        results = [dict(row) for row in cursor.fetchall()]
        return results
    #==订单查询==
    def get_order(self,order_id:str)->Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM orders WHERE order_id=?",(order_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    #==物流查询==
    def get_logistics(self,tracking:str)->Optional[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM logistics WHERE tracking=?",(tracking,))
        row = cursor.fetchone()
        return dict(row) if row else None
    #==对话历史==
    def save_conversation(self,session_id:str,role:str,content:str,intent:str=None):
        self.conn.execute("INSERT INTO conversations(session_id, msg_role, content,intrny)VALUES (?,?,?,?)",(session_id,role,content,intent))
        self.conn.commit()

    def get_conversations(self,session_id:str,limit:int=20)->List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT msg_role,content FROM conversations WHERE session_id = ? ORDER BY created_at DESC LIMIT ?",(session_id,limit))
        return [dict(row) for row in reversed(cursor.fetchall())]
#全局单例
db = DataManager()