from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service


class Login:
    def __init__(self, chromedriver_path, url):
        self.chromedriver_path = chromedriver_path
        self.url = url
        self.driver = None

    def setup_driver(self):
        service = Service(executable_path=self.chromedriver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.url)

    def login(self, username, password):
        username_site = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        username_site.send_keys(username)
        password_site = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_site.send_keys(password)
        check_box = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='app']/div/div/form/div[5]/label/span[1]"))
        )
        self.driver.execute_script("arguments[0].click();", check_box)
        login_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//button/span[contains(normalize-space(),"立即登录")]'))
        )
        yzm_site = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/form/div[2]/div/div/div/div/input'))
        )
        max_tries = 3
        for i in range(max_tries):
            try:
                yzm = input("请查看验证码以后输入，点击enter: ")

                # 清空并输入验证码
                yzm_site.send_keys(Keys.CONTROL, "a")
                yzm_site.send_keys(Keys.DELETE)
                yzm_site.send_keys(yzm)
                sleep(1)
                self.driver.execute_script("arguments[0].click();", login_btn)

                # 检查是否出现错误提示
                try:
                    error_msg = WebDriverWait(self.driver, 1).until(
                        EC.presence_of_element_located((By.XPATH, '//div[contains(., "无效的验证码")]'))
                    )
                    if "无效的" in error_msg.text:
                        print(f"验证码错误，还剩 {max_tries - i - 1} 次尝试")
                        continue
                except:
                    # 没有错误提示，说明登录成功
                    print("登录成功")
                    break
            except:
                print(f"验证码输入错误，还剩 {max_tries - i - 1} 次尝试")
                continue
        else:
            print("登录失败，请检查用户名和密码")
            self.driver.quit()
            exit()

        button1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/section/aside/div/div/div/div/div/div[2]'))
        )
        self.driver.execute_script("arguments[0].click();", button1)
        button2 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="app"]/section/aside/div/div/div/div/div/div[3]/div/div[2]/div[3]/div/div/div/a'))
        )
        self.driver.execute_script("arguments[0].click();", button2)
        button3 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div/div[2]/div[1]/button/span'))
        )
        self.driver.execute_script("arguments[0].click();", button3)

    def close_driver(self):
        self.driver.quit()


class Operation:
    def __init__(self, driver):
        self.driver = driver

    def add(self, hj_id, hj_port):
        button1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="app"]/section/aside/div/div/div/ul/div/li[1]/span[contains(normalize-space(), "数据汇集")]'))
        )
        self.driver.execute_script("arguments[0].click();", button1)
        new_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="content"]/div[1]/div[1]/div/div/div/div/div[2]/div[1]/button/span[contains(normalize-space('
                '), "创建任务")]'))
        )
        self.driver.execute_script("arguments[0].click();", new_button)
        hj_id_site = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="content"]/div[2]/div/div[2]/div/div/div[2]/form/div[1]/div[1]/div/div[2]/div/div/div/input'))
        )
        hj_id_site.send_keys(hj_id)
        msg_type_site = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="content"]/div[2]/div/div[2]/div/div/div[2]/form/div[2]/div[1]/div/div[2]/div/div/div'))
        )
        msg_type_site.click()
        msg_type_site1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[2]/div/div/div/ul/li[1]'))
        )
        self.driver.execute_script("arguments[0].click();", msg_type_site1)
        hj_port_site = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="content"]/div[2]/div/div[2]/div/div/div[2]/form/div[5]/div/div/div[2]/div/div/div/input'))
        )
        hj_port_site.send_keys(hj_port)
        hj_status_site = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="content"]/div[2]/div/div[2]/div/div/div[2]/form/div[7]/div/div/div[2]/div/label/span[1]'))
        )
        hj_status_site.click()
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="content"]/div[2]/div/div[2]/div/div/div[3]/div/button[2]/span[contains(normalize-space(), '
                '"确认")]'))
        )
        self.driver.execute_script("arguments[0].click();", submit_btn)


if __name__ == '__main__':
    url = "http://58.49.94.131:18500/sw/#/login"
    chromedriver_path = r'C:/Program Files/JetBrains/PyCharm Community Edition 2023.1.2/bin/chromedriver.exe'
    login = Login(chromedriver_path, url)
    login.setup_driver()
    login.login("111", "111")
    operation = Operation(login.driver)
    operation.add("hj8000", "8000")
    sleep(5)
    login.close_driver()
