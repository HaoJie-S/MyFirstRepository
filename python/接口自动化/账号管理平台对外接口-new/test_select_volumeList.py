import requests


# 测试查询兑换码列表
class TestAccount:
    def test_ty_select_volumeList(self):
        """测试查询兑换码列表"""
        url = "http://58.49.94.131:18389/web/api/v2/volume/list"
        json_data = {
            "accessMethod": "",
            "volumeType": "",
            "duration": "1",
            "diffAccount": "",
            "isExclusive": ""
        }
        # headers = {"token": auth_token}
        headers = {"token": "ASLCJISACD4641684SAD"}

        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()

        print(f"\n📊 天元位置服务-查询所有兑换码:")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        print(f"  数据条数：{len(result['list'])}")
        import json
        print(f"  啥玩意数据：{json.dumps(result['list'], ensure_ascii=False, indent=2)}")

        # if 'data' in result:
        #     print(f"  数据条数: {len(result['list'])}")

        assert response.status_code == 200
