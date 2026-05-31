from api_utils import *
from config import *


class TestChangePassword:
    def test_change_password(self):
        """修改密码"""
        json_data = {
            "diffAccount": TEST_ACCOUNTS["changed_password_diffAccount"],
            "password": TEST_ACCOUNTS["password"]
        }
        response,result = post_request(
            url=CHANGE_PASSWORD_URL,
            json_data=json_data,
            test_name="账号管理平台对外接口:修改密码"
        )
        print(f"  返回的所有数据{result}")
        if result.get("code") != 200:
            print(f"  错误信息: {result.get('msgerr')}")
        print(f"  响应对象: {response}")
        check_response(response, result)