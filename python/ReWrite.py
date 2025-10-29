from selenium.webdriver.support import expected_conditions as EC
from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait


class LoginAndOpreation:
    def __init__(self, chrome_driver_path, url):
        self.driver = None  # 先占位，后面再初始化
        self.url = url
        self.chrome_driver_path = chrome_driver_path

    def setup_driver(self):
        service = Service(executable_path=self.chrome_driver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.url)
        self.driver.maximize_window()

    def login(self):
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h3[contains(text(),"欢迎")]'))
        )
        sleep(2)
        right_page = self.driver.find_element(By.XPATH, '//a[text()="账号密码登录"]')
        if right_page:
            right_page.click()
        username = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, 'username'))
        )
        password = self.driver.find_element(By.NAME, "password")
        yzm = self.driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入图形验证码"]')
        agreee_btn = self.driver.find_element(By.CSS_SELECTOR, 'span.t-checkbox__input')
        login_buton = self.driver.find_element(By.XPATH, '//button/span[text()="立即登录"]/..')
        username.send_keys("102")
        password.send_keys("8808")
        agreee_btn.click()

        max_retries = 3
        retry_count = 0
        while retry_count < max_retries:
            captch_input = input("请在浏览器查看验证码，然后控制台输入，按回车结束")
            yzm.send_keys(Keys.CONTROL, "a")
            yzm.send_keys(Keys.DELETE)
            yzm.send_keys(captch_input)
            login_buton.click()
            try:
                error_msg = WebDriverWait(self.driver, 1).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"无效的验证码")]'))
                )
                if "无效" in error_msg.text:
                    print("验证码错误，请重新输入")
                    retry_count += 1
                    continue
                else:
                    print("登录成功")
                    break
            except:
                print("未出现无效验证码提示")
                break

        if retry_count >= max_retries:
            exit()

    def login_operation(self):
        choice1 = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.top-nav-btn'))
        )
        choice1.click()
        user_dev = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//a[contains(normalize-space(),"账号管理平台(dev用户)")]'))
            # //normalize-space()作用是去除空格
        )
        user_dev.click()
        MakeSure = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//span[contains(normalize-space(),"确认授权")]'))
        )
        MakeSure.click()
        sleep(10)

    def quit_driver(self):
        self.driver.quit()

    # +++++++++++++++++++++++++++++++++++++++++++++++++++++


if __name__ == '__main__':
    chrome_driver_path = r'C:\Program Files\JetBrains\PyCharm Community Edition 2023.1.2\bin\chromedriver.exe'
    url = "http://58.49.94.131:30082/kplsso-dev/#/login"

    login_operate = LoginAndOpreation(chrome_driver_path, url)
    login_operate.setup_driver()
    login_operate.login()
    login_operate.login_operation()

    login_operate.quit_driver()  # 退出浏览器
