import csv
from time import sleep

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class Login:
    def __init__(self, chromedriver_path, url):
        self.chromedriver_path = chromedriver_path
        self.url = url
        self.driver = None

    def setup_driver(self):
        service = Service(executable_path=self.chromedriver_path)
        self.driver = webdriver.Chrome(service=service)
        self.driver.get(self.url)
        self.driver.maximize_window()

    def login(self, username, password):
        # 保障页面加载完成
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//h3[contains(text(), "欢迎使用")]'))
        )
        sleep(2)
        page = self.driver.find_element(By.XPATH, '//a[text()="账号密码登录"]')
        # 如果page按钮存在，就点击，没有就不管
        if page:
            page.click()
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
                '//*[@id="content"]/div[2]/div/div[2]/div/div/div[2]/form/div[2]/div[1]/div/div['
                '2]/div/div/div/div/div/input'))
        )
        self.driver.execute_script("arguments[0].click();", msg_type_site)
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
        self.driver.execute_script("arguments[0].click();", hj_status_site)
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="content"]/div[2]/div/div[2]/div/div/div[3]/div/button[2]/span[contains(normalize-space(), '
                '"确认")]'))
        )
        self.driver.execute_script("arguments[0].click();", submit_btn)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[3]/div/div[contains(normalize-space(), "添加成功")]'))
        )

    @staticmethod
    def read_tasks_from_csv(filename='tasks.csv'):
        tasks = []
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # 跳过标题行

            for row in reader:
                if len(row) >= 2:
                    hj_id = row[0].strip()  # 第一列
                    hj_port = row[1].strip()  # 第二列
                    tasks.append((hj_id, hj_port))

        return tasks

    def add_tasks_from_csv(self, filename):
        filename = 'E:/code/MyFirstRepository/python/tasks.csv'
        tasks = self.read_tasks_from_csv(filename)
        for hj_id, hj_port in tasks:
            self.add(hj_id, hj_port)
            sleep(1)  # 建议添加延迟

    def delete(self):
        button1 = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '//*[@id="app"]/section/aside/div/div/div/ul/div/li[1]/span[contains(normalize-space(), "数据汇集")]'))
        )
        self.driver.execute_script("arguments[0].click();", button1)
        delete_btn = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH, '//*[@id="content"]/div[1]/div[2]/div/div/div/div/div/div[1]/table/tbody/tr[1]/td['
                          '14]/div/div[2]/a'))
        )
        self.driver.execute_script("arguments[0].click();", delete_btn)
        submit_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((
                By.XPATH, "(//div/div[contains(normalize-space(), '是否删除')])[1]/parent::div/button/span[contains("
                          "normalize-space(), '确认')]"))
        )
        self.driver.execute_script("arguments[0].click();", submit_btn)
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((
                By.XPATH,
                '/html/body/div[3]/div/div[contains(normalize-space(), "删除成功")]'))
        )


if __name__ == '__main__':
    url = "http://58.49.94.131:18500/sw/#/login"
    chromedriver_path = r'C:/Program Files/JetBrains/PyCharm Community Edition 2023.1.2/bin/chromedriver.exe'
    login = Login(chromedriver_path, url)
    login.setup_driver()
    login.login("111", "111")
    operation = Operation(login.driver)
    # operation.add(8888, 8888)
    # hj_id = 8000
    # hj_port = 8000
    # for i in range(3):
    #     try:
    #         operation.add(hj_id, hj_port)
    #         hj_id += 1
    #         hj_port += 1
    #         continue
    #     except:
    #         print(f"第{i + 1}次尝试失败，重试中...")
    # print("=== 使用CSV文件批量添加任务 ===")
    operation.add_tasks_from_csv("tasks.csv")
    for i in range(3):
        operation.delete()
    login.close_driver()
