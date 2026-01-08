import requests


# 测试查询所有的账号
class TestAccount:
    def test_select_all_accounts(self, auth_token):
        """测试查询所有账号"""
        url = "https://s.kplgnss.com/wxw/api/web/v2/v2/changeaccpass"
        json_data = {
            "diffAccount": "bjxt022",
            "password": "123"
        }
        # headers = {"token": auth_token}
        headers = {"token": "9F7AC3995E176AD9CA"}

        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()

        print(f"\n📊 天元位置服务-修改密码结果:")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        # print(f"  数据条数: {result.get('list')}")
        print(f"  旧密码: {result['oldPass']}")
        print(f"  新密码: {result['nowPass']}")

        # if 'data' in result:
        #     print(f"  数据条数: {len(result['list'])}")

        assert response.status_code == 200
