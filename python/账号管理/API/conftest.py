import pytest
import requests


@pytest.fixture(scope="session", autouse=True)
def auth_token():
    """获取认证token（整个测试会话只获取一次）"""
    print("\n" + "=" * 50)
    print("正在获取认证token...")

    url = "https://s.kplgnss.com/wxw/api/web/v2/wx/token"
    ticket = "CFLzSR4HJQQlEjEDWNF3qJmuT6KrloKilm3ecMaC33zCmrmcobqD1GrqSA"

    response = requests.post(url, json={"ticket": ticket})

    if response.status_code != 200:
        pytest.fail(f"获取token失败: {response.status_code}")

    result = response.json()

    if result.get("code") != 0:
        pytest.fail(f"业务失败: {result}")

    token = result.get("token")
    if not token:
        pytest.fail("响应中没有token")

    print(f"✅ 获取token成功: {token[:20]}...")
    print("=" * 50 + "\n")
    assert response.status_code == 200

    return token
