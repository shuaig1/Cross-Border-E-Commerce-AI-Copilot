from langchain.tools import tool
import random

@tool
def generate_promp_email(user_name:str,interest:str=" ")->str:
    """
    为指定用户生成一封个性化的促销邮件。
    输入:user_name(用户名称),interest(可选，用户感兴趣的商品品类)
    返回:完整的邮件标题和正文
    """
    templates = [
        {
            "subject": f"🔥 {user_name}，你的专属折扣已到账！",
            "body": f"Hi {user_name}，感谢你一直以来的支持。为你准备了一张 **8 折优惠券**，全站通用，结账时输入 **WELCOME20** 即可享受。快来挑选心仪的商品吧！"
        },
        {
            "subject": f"🎁 {user_name}，你有一份礼物待领取",
            "body": f"Hi {user_name}，我们注意到你最近浏览了{interest if interest else '不少商品'}，特地为你准备了一份小礼物。下单时使用 **GIFT15** 可享 **85 折**，限时有效哦。"
        },
        {
            "subject": f"💌 {user_name}，别让你的心愿单落空",
            "body": f"Hi {user_name}，你的购物车里还有未结算的商品吗？现在就清空购物车，结账时输入 **SAVE10** 立减 **$10**，只限今天！"
        }
    ]
    email = random.choice(templates)
    return f"邮件标题:{email['subject']}\n\n邮件正文:\n{email['body']}"
@ tool
def recall_abandoned_cart(user_name:str,last_item:str=" ")->str:
    """
    生成弃购召回话术。针对将商品加入购物车但未付款的用户。
    输入：user_name（用户名称），last_item（最后加入购物车的商品名）
    返回：适合通过邮件或站内信发送的召回文案
    """
    return (
        f"Hi {user_name}，看到你曾把“{last_item if last_item else '心仪的商品'}”加入购物车，是遇到什么问题了吗？"
        f"现在下单即可享 **免费配送** 和 **30 天无忧退换**。别错过哦，库存不多了！"
        f"\n\n👉 [点击这里回到购物车]"
    )