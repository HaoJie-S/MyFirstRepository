from selenium.webdriver.common.by import By


def debug_dom_structure(self):
    """调试DOM结构"""
    # 查看页面HTML源码
    page_source = self.driver.page_source
    print("📄 页面HTML长度:", len(page_source))

    # 查找所有span元素的文本
    spans = self.driver.find_elements(By.TAG_NAME, "span")
    print(f"🔍 当前DOM中有 {len(spans)} 个span元素")

    # 打印包含特定关键词的span
    for span in spans:
        text = span.text.strip()
        if text and ("RTCM" in text.upper() or "3.X" in text.upper()):
            print(f"✅ 找到相关span: '{text}'")

    # 检查是否有iframe
    iframes = self.driver.find_elements(By.TAG_NAME, "iframe")
    print(f"🖼️ 页面中有 {len(iframes)} 个iframe")