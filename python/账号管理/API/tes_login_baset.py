import requests


def test_post_request():
    url1 = "https://s.kplgnss.com/wxw/api/web/v2/wx/token"
    form_data = {
        "ticket": "CFLzSR4HJQQlEjEDWNF3qJmuT6KrloKilm3ecMaC33zCmrmcobqD1GrqSA"
    }

    # 1. 发送表单格式（form-data）的POST请求
    response1 = requests.post(url=url1, data=form_data)

    json_data = {
        "ticket": "CFLzSR4HJQQlEjEDWNF3qJmuT6KrloKilm3ecMaC33zCmrmcobqD1GrqSA",
    }

    # 2. 发送JSON格式的POST请求（推荐，目前大多数接口采用此格式）
    response2 = requests.post(url=url1, json=json_data)

    # 解析响应结果
    print("=== 表单格式POST请求响应结果 ===")
    print("响应状态码：", response1.status_code)
    print("响应正文（JSON格式）：", response1.json())

    print("\n=== JSON格式POST请求响应结果 ===")
    print("响应状态码：", response2.status_code)
    print("响应正文（JSON格式）：", response2.json())
