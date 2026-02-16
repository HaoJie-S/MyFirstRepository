import requests


# 测试查询操作日志
class TestOperationRecord:
    def test_ty_change_password(self):
        """修改指定账号密码"""
        url = 'http://58.49.94.131:18389/web/api/v2/changeaccpass'
        json_data = {
            "diffAccount": "23qn8031",
            "password": "123"
        }
        headers = {
            "token": "ASLCJISACD4641684SAD"
        }
        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()
        print("📊 账号管理平台对外接口:修改差分账号密码")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        print(f"  原密码：{result.get('oldPass')}")
        print(f"  新密码：{result.get('nowPass')}")
        # print(f"  数据条数: {len(result['list'])}")
        assert response.status_code == 200
