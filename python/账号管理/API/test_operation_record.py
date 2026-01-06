import requests


class TestOperationRecord:
    def test_get_operation_record(self, auth_token):
        """查询有关设备的操作记录"""
        url = 'https://s.kplgnss.com/wxw/api/web/v2/v2/device/acc/renew/list'
        json_data = {
            "deviceId": "123",
            "category": 1
        }
        headers = {
            "token": "9F7AC3995E176AD9CA"
        }
        response = requests.post(url, json=json_data, headers=headers)
        result = response.json()
        print("📊 操作记录查询结果:")
        print(f"  状态码: {response.status_code}")
        print(f"  业务码: {result.get('code')}")
        print(f"  数据条数: {len(result['list'])}")
        assert response.status_code == 200
