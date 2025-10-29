from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LoginAndOpeatipn:
    def __init__(self, chrome_driver_path, url):
        self.driver = None
        self.chrome_driver_path = chrome_driver_path
        self.url = url

    def setup_driver(self):
        service = Service(executable_path=self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.url)
        # self.driver.maximize_window()

    def login(self):
        username = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password = self.driver.find_element(By.NAME, 'password')
        check_agreement = self.driver.find_element(By.CSS_SELECTOR, 'span.t-checkbox__input')
        yzm = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入图形验证码"]')
        # self.driver.execute_script("agreementBtn.click();", check_agreement)
        check_agreement.click()
        username.send_keys("admin")
        password.send_keys("8808")
        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            captcha_input = input("请在浏览器查找验证码并输入，然后按回车继续")
            yzm.send_keys(Keys.CONTROL, "a")
            yzm.send_keys(Keys.DELETE)
            yzm.send_keys(captcha_input)

            login_button = self.driver.find_element(By.XPATH, '//button/span[contains(normalize-space(),"立即登录")]')
            login_button.click()
            try:
                error_msg = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"无效的验证码")]'))
                )
                if "无效" in error_msg.text:
                    print("验证码错误，请重新输入")
                    retry_count += 1
                    if retry_count == max_retries:
                        print("验证码错误次数过多，退出登录")
                        break
                    continue
                else:
                    print("登录成功")
                    break
            except:
                print("登录成功?")
                break
        choice = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.top-nav-btn'))
        )
        choice.click()
        choice2 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//a[text()="单基站"]'))
        )
        self.driver.execute_script("arguments[0].click();", choice2)
        shouquan = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button/span[text()="确认授权"]'))
        )
        shouquan.click()
        # 点击数据采集菜单（假设这部分是正确的）
        data_collection = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//li[@class='t-menu__item'][1]"))
        )
        data_collection.click()

    # 创建一个汇集任务
    def add(self):
        add1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[contains(@class, 't-button--theme-primary')]//span[text()='创建任务']"))
        )
        add1.click()
        sleep(2)
        collect_name = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//label[text()='汇集任务名称']/following::input[@class='t-input__inner']"
            ))
        )
        collect_name.send_keys("bf0001")
        message_type = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//label[text()='数据格式']/following::input[@class='t-input__inner']"
                ))
        )
        message_type.click()

        geshi = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[text()='RTCM 3.x']"))
        )
        self.driver.execute_script("arguments[0].click();", geshi)
        sleep(1)

        exit = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                "//button/span[contains(normalize-space(),'取消')]"
            ))
        )
        self.driver.execute_script("arguments[0].click();", exit)
        sleep(2)

    def open_close(self):
        # 步骤1：定位第一个tr
        first_tr = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//tbody/tr[1]"))  # 定位tbody下的第一个tr
        )
        # 步骤2：在第一个tr内定位“编辑”链接
        edit_link = first_tr.find_element(
            By.XPATH,
            ".//a[text()='编辑' and contains(@class, 't-link--theme-primary')]"
        )
        self.driver.execute_script("arguments[0].click();", edit_link)
        sleep(1)
        open_close = self.driver.find_element(By.XPATH, "//span[contains(normalize-space(),'开启')]")
        self.driver.execute_script("arguments[0].click();", open_close)
        sleep(1)
        make_sure = self.driver.find_element(By.XPATH, "//button/span[text()='确认']")
        self.driver.execute_script("arguments[0].click();", make_sure)

    def close_driver(self):
        self.driver.quit()

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


if __name__ == '__main__':
    login_url = "http://119.96.209.132:18081/sw/#/login"
    chrome_driver_path = r'C:\Program Files\JetBrains\PyCharm Community Edition 2023.1.2\bin\chromedriver.exe'
    login_and_open = LoginAndOpeatipn(chrome_driver_path, login_url)
    login_and_open.setup_driver()
    login_and_open.login()
    # login_and_open.debug_dom_structure()
    # login_and_open.add()
    # a = 1
    # while a < 20:
    #     login_and_open.open_close()
    #     a += 1
    #     sleep(2)
    login_and_open.close_driver()
