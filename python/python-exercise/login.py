from selenium.webdriver import Keys
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver
from time import sleep

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

# 获取浏览器对象
# 1. 指定 chromedriver.exe 的路径
chrome_driver_path = r'C:\Program Files\JetBrains\PyCharm Community Edition 2023.1.2\bin\chromedriver.exe'

# 2. 创建 Service 对象
service = Service(executable_path=chrome_driver_path)  # 注意：这里用的是 Service 的 executable_path

# 3. 创建 Chrome WebDriver 实例
driver = webdriver.Chrome(service=service)  # 注意传入的是 service 对象
# driver = webdriver.Firefox()

# 4. 打开网页
# 打开url(本地文件)
url = "http://58.49.94.131:30082/kplsso-dev/#/login"
driver.get(url)

# 保障页面加载完成
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//h3[contains(text(), "欢迎使用")]'))
)
sleep(2)
page = driver.find_element(By.XPATH, '//a[text()="账号密码登录"]')
# 如果page按钮存在，就点击，没有就不管
if page:
    page.click()

# 查找是否为账号密码登录


# 等待页面加载完成  直到找到指定的元素
# 等待元素加载完成
# 等待元素可见
username = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, 'username'))
)
# password=WebDriverWait(driver, 10).until(
#     EC.presence_of_element_located(By.NAME,'password')
# )
# sleep(3)
# 查找用户名元素
# username = driver.find_element(By.NAME, 'username')
# 查找密码元素
password = driver.find_element(By.NAME, 'password')
# 查找验证码元素
yzm = driver.find_element(By.CSS_SELECTOR, 'input[placeholder="请输入图形验证码"]')
# 用户名输入102  send_keys('内容')
username.send_keys("102")
# 密码输入123456
password.send_keys("8808")
# 点击同意协议
# agree_btn = driver.find_element(By.CSS_SELECTOR, 'label[tabindex="0"]')
agree_btn = driver.find_element(By.CSS_SELECTOR, 'span.t-checkbox__input')
agree_btn.click()

# 验证码输入
# captcha_input = input("请在浏览器中查看验证码，手动输入后，按回车键继续...")
# yzm.send_keys(captcha_input)
max_retries = 3
retry_count = 0
while retry_count < max_retries:
    captcha_input = input("请在浏览器中查看验证码，手动输入后，按回车键继续...")
    # yzm.clear()
    yzm.send_keys(Keys.CONTROL, 'a')  # 全选
    yzm.send_keys(Keys.DELETE)  # 删除
    yzm.send_keys(captcha_input)
    # 点击登录按钮
    login_btn = driver.find_element(By.XPATH, '//button/span[text()="立即登录"]/..')
    login_btn.click()
    # 检查验证码是否正确有提示
    try:
        error_msg = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"无效的验证码")]'))
        )
        if "无效的验证码" in error_msg.text:
            print("验证码错误，请重新输入")
            retry_count += 1
            continue
        else:
            print("登录成功")
            break
    except:
        print("登录成功")
        break

if retry_count >= max_retries:
    print(f"已连续 {max_retries} 次验证码错误，停止尝试。")
    driver.quit()
    exit()

# 等待页面加载完成
input("请在浏览器中查看是否登录成功，按回车键退出...")
choice1 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.top-nav-btn'))
)
# 不会检查元素是否可见，只会检查元素是否存在，比较方便使用
driver.execute_script("arguments[0].click();", choice1)
# choice1.click()
sleep(1)
# 选择账号管理平台(dev用户)   By.XPATH要用//    一个整体两个（（））
choiceDEV = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//a[text()="账号管理平台(dev用户)"]'))
)
driver.execute_script("arguments[0].click();", choiceDEV)
# 点击确认授权
shouQuan = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//button/span[text()="确认授权"]'))
)
driver.execute_script("arguments[0].click();", shouQuan)
sleep(1)
# 退出浏览器
driver.quit()
