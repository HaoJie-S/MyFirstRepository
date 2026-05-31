import requests
from config import ACTIVE_ACCOUNT_URL, TEST_ACCOUNTS, HEADERS
from api_utils import post_request, check_response


# 测试查询操作日志
class TestOperationRecord:
    def test_ty_active_account(self):
        """激活指定差分账号"""
        # 使用配置文件中的URL和账号
        json_data = {
            "diffAccount": TEST_ACCOUNTS["active"]  # 从配置中获取
        }

        # 使用统一的请求函数
        response, result = post_request(
            url=ACTIVE_ACCOUNT_URL,
            json_data=json_data,
            test_name="账号管理平台对外接口:激活差分账号"
        )

        # 特殊处理：打印错误信息
        if result.get("code") != 200:
            print(f"  错误信息: {result.get('msgerr')}")

        # 打印完整的response对象（保持你原来的调试方式）
        print(f"  响应对象: {response}")

        # 使用统一的检查函数
        check_response(response, result)