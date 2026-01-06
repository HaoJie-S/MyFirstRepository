import requests


class TestAccount:
    def test_select_all_accounts(self, auth_token):
        """测试查询所有账号"""
        url = "https://s.kplgnss.com/wxw/api/web/v2/v2/device/acclist"
        json_data = {"args": "", "pageNum": 1, "pageSize": 10}
        headers = {"token": auth_token}

        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()

        print(f"📊 查询账号列表结果:")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        print(f"  消息: {result.get('msg')}")

        if 'data' in result:
            print(f"  数据条数: {len(result['data'])}")

        assert response.status_code == 200
