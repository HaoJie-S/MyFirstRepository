"""
简单的API请求工具
只封装最基本的通用功能
"""
import requests

from config import *


def post_request(url, json_data, headers=None, test_name=""):
    """
    发送POST请求的通用函数
    :param url: 完整的接口URL
    :param json_data: 请求体数据
    :param headers: 请求头（不传则使用默认）
    :param test_name: 测试名称（用于打印）
    :return: (response, result) 响应对象和解析后的数据
    """
    # 使用传入的headers或默认headers
    request_headers = headers if headers else HEADERS

    # 发送请求
    response = requests.post(
        url=url,
        json=json_data,
        headers=request_headers,
        timeout=TIMEOUT
    )

    # 解析响应
    try:
        result = response.json()
    except:
        result = {"text": response.text}

    # 打印信息（保持你原来的格式）
    if test_name:
        print(f"\n📊 {test_name}")
        print(f"  状态码: {response.status_code}")
        if isinstance(result, dict):   # 如果result是字典类型（说明可能是JSON）
            print(f"  业务码: {result.get('code', 'N/A')}")
            print(f"  返回信息: {result.get('msg', 'N/A')}")

    return response, result


def check_response(response, result, expected_code=200):
    """
    检查响应的通用函数
    :param response: 响应对象
    :param result: 解析后的响应数据
    :param expected_code: 期望的HTTP状态码
    """
    # 检查HTTP状态码
    assert response.status_code == expected_code, f"HTTP状态码错误: {response.status_code}"

    # 如果有业务码，也检查
    if isinstance(result, dict) and 'code' in result:
        if result.get('code') != 200:
            print(f"  错误详情: {result.get('msgerr', 'N/A')}")
