import requests


# 测试查询操作日志
class TestOperationRecord:
    def test_ty_active_account(self):
        """激活指定得差分账号"""
        url = 'http://58.49.94.131:18389/web/api/v2/activeacc'
        json_data = {
            "diffAccount": "23qn8021"
        }
        headers = {
            "token": "ASLCJISACD4641684SAD"
        }
        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()
        print("📊 账号管理平台对外接口:激活差分账号")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        print(f"  返回信息：{result.get('msg')}")
        if result.get("code") != 200:
            print(f"  返回信息：{result.get('msgerr')}")
        # print(f"  数据条数: {len(result['list'])}")
        print(response)
        assert response.status_code == 200
