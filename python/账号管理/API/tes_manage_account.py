# import requests
#
#
# class TestLogin:
#     def setup_method(self):
#         self.url = "https://s.kplgnss.com/wxw/api/web/v2/wx/token"
#         self.ticket = "CFLzSR4HJQQlEjEDWNF3qJmuT6KrloKilm3ecMaC33zCmrmcobqD1GrqSA"
#
#     def test_login(self):
#         json_data = {
#             "ticket": self.ticket
#         }
#         response = requests.post(url=self.url, json=json_data)
#         result = response.json()
#         assert response.status_code == 200, f"请求失败，返回的状态码为{response.status_code}"
#         assert "token" in result, "请求失败，返回的结果中没有token字段"
#         self.token = result.get("token")
#         # print(f"\ntoken的值为：{self.token}")
#
#     def test_select_all_accounts(self):
#         self.url = "https://s.kplgnss.com/wxw/api/web/v2/v2/device/acclist"
#         json_data = {
#             "args": "",
#             "pageNum": 1,
#             "pageSize": 10
#         }
#         headers = {
#             # "token": self.token
#             "token": "9F7AC3995E176AD9CA"
#         }
#         response = requests.post(url=self.url, json=json_data, headers=headers)
#         assert response.status_code == 200, f"请求失败，返回的状态码为{response.status_code}"
