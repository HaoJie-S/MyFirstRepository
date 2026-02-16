import requests


# 测试查询操作日志
class TestOperationRecord:
    def test_ty_change_password(self):
        """修改指定账号密码"""
        url = 'http://58.49.94.131:18389/web/api/v2/acc/volume/renew'
        json_data = {
            "diffAccount": "23qn8021",
            "itms": [
                {
                    "volumeDuration": 1,
                    "volumeType": 0,
                    "serviceid": "",
                    "accessmethod": "ntrip",
                    "num": 1
                }
            ]
        }
        headers = {
            "token": "ASLCJISACD4641684SAD"
        }
        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()
        print("📊 账号管理平台对外接口:选定差分账号续费")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        print(f"  结果：{result.get('msg')}")
        print(f"  续费账号：{result.get('success')}")
        # print(f"  数据条数: {len(result['list'])}")
        assert response.status_code == 200
