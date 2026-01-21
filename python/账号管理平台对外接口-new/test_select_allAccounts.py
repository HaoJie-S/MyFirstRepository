import requests


# 测试查询所有的账号
class TestAccount:
    def test_activate_accounts(self):
        """测试查询所有账号"""
        url = "http://58.49.94.131:18389/web/api/v2/acclist"
        json_data = {
            "diffAccount": "",
            "diffAccountStatus": 2,
            "pageNum": 1,
            "pageSize": 61
        }
        # headers = {"token": auth_token}
        headers = {"token": "ASLCJISACD4641684SAD"}

        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()

        print(f"\n📊 天元位置服务-查询所有账号结果:")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        print(f"  数据条数：{len(result['list'])}")
        print(f"  总条数: {result['allCount']}")

        # if 'data' in result:
        #     print(f"  数据条数: {len(result['list'])}")

        assert response.status_code == 200
