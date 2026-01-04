from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from selenium.webdriver.support.wait import WebDriverWait


def delete(self):
    print("🔍 步骤1: 开始删除操作")  # 添加调试信息

    # 步骤1：定位第一个tr
    first_tr = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]"))
    )
    print("✅ 步骤1完成: 找到第一个表格行")

    # 步骤2：在第一个tr内定位“删除”链接
    print("🔍 步骤2: 查找删除链接")
    edit_link = first_tr.find_element(By.XPATH, ".//a[text()='删除']")
    print("✅ 步骤2完成: 找到删除链接")

    # 步骤3：点击删除链接
    print("🔍 步骤3: 点击删除链接")
    self.driver.execute_script("arguments[0].click();", edit_link)
    print("✅ 步骤3完成: 已点击删除链接")

    # 步骤4：等待确认按钮出现
    print("🔍 步骤4: 等待确认按钮")
    make_sure_delete = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button/span[text()='确认']"))
    )
    print("✅ 步骤4完成: 找到确认按钮")

    # 步骤5：点击确认按钮
    print("🔍 步骤5: 点击确认按钮")
    self.driver.execute_script("arguments[0].click();", make_sure_delete)
    print("✅ 步骤5完成: 删除操作完成")

    sleep(5)


def delete1(self):
    try:
        # 检查页面中有多少个删除链接
        all_delete_links = self.driver.find_elements(By.XPATH, "//a[text()='删除']")
        print(f"🔍 调试信息: 页面中共有 {len(all_delete_links)} 个删除链接")

        # 检查第一个表格行
        first_tr = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]"))
        )

        # 检查第一个tr中有多少删除链接
        tr_delete_links = first_tr.find_elements(By.XPATH, ".//a[text()='删除']")
        print(f"🔍 调试信息: 第一个表格行中有 {len(tr_delete_links)} 个删除链接")

        if len(tr_delete_links) == 0:
            print("❌ 错误: 第一个表格行中没有删除链接!")
            return False

        # 继续执行删除操作...

    except Exception as e:
        print(f"❌ 异常信息: {e}")
