import pytest as pytest
import requests
import sys


class TestLogin:
    def setup_method(self):
        self.url = "https://s.kplgnss.com/wxw/api/web/v2/wx/token"
        self.ticket = "CFLzSR4HJQQlEjEDWNF3qJmuT6KrloKilm3ecMaC33zCmrmcobqD1GrqSA"

    def test_post_request(self):
        # 发送POST请求
        # 1. 发送表单格式（form-data）的POST请求
        # response1 = requests.post(url=self.url, data={"ticket": self.ticket})

        json_data = {
            "ticket": self.ticket,
        }

        # 2. 发送JSON格式的POST请求（推荐，目前大多数接口采用此格式）
        response2 = requests.post(url=self.url, json=json_data)

        # 解析响应结果
        # print("=== 表单格式POST请求响应结果 ===")
        # print("响应状态码：", response1.status_code)
        # print("响应正文（JSON格式）：", response1.json())
        #
        # print("\n=== JSON格式POST请求响应结果 ===")
        # print("响应状态码：", response2.status_code)
        # print("响应正文（JSON格式）：", response2.json())
        #
        # assert response2.status_code == 200
        # print(f"✅ 状态码验证通过: {response2.status_code}")

        # 更详细的验证
        if response2.status_code == 200:
            print("请求成功")
        elif response2.status_code == 400:
            print("客户端错误：参数错误")
        elif response2.status_code == 401:
            print("认证失败")
        elif response2.status_code == 500:
            print("服务器内部错误")


# if __name__ == '__main__':
#     sys.exit(pytest.main(["-s", "test_login.py"]))

