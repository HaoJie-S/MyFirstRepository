"""
统一配置文件 - 所有需要修改的变量都放在这里
使用时直接导入即可：from config import *
"""
# =================== 基础配置 ===================
# 基础URL - 只需修改这里，所有测试URL都会自动更新
BASE_URL = "http://58.49.94.131:18389"

# API前缀 - 如果所有接口都有相同前缀
API_PREFIX = "/web/api/v2"

# Token - 统一在这里修改
TOKEN = "ASLCJISACD4641684SAD"

# =================== 完整的API URL ===================
# 创建完整的接口URL，方便直接使用
ACTIVE_ACCOUNT_URL = f"{BASE_URL}{API_PREFIX}/activeacc"
CHANGE_PASSWORD_URL = f"{BASE_URL}{API_PREFIX}/changeaccpass"
RENEW_ACCOUNT_URL = f"{BASE_URL}{API_PREFIX}/acc/volume/renew"

# =================== 统一的请求头 ===================
HEADERS = {
    "token": TOKEN,
    "Content-Type": "application/json"
}

# =================== 其他全局配置 ===================
# 超时时间（秒）
TIMEOUT = 10

# 测试账号（可以统一管理）
TEST_ACCOUNTS = {
    "active": "23qn8022",
    "changed_password_diffAccount": "23qn8031",
    "password": "123",
    "renew": "23qn8021"
}
