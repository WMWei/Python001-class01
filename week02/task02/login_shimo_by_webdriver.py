from selenium import webdriver
# 用于等待页面加载
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class ShiMo:
    def __init__(self, data):
        self.home_url = 'https://shimo.im/welcome'
        # 初始化webdriver
        chrome_op = webdriver.ChromeOptions()
        chrome_op.add_argument('--headless')
        chrome_op.add_argument('--disable-gpu')
        self.driver = webdriver.Chrome(options=chrome_op)
        # 设置隐式等待，在可能需要等待的地方进行轮询
        # self.driver.implicitly_wait(30)  # seconds
        self.data = data

    def login(self):
        self.driver.get(self.home_url)
        self.driver.find_element_by_xpath(
            #"//button[contains(@class, 'login-button')]"
            "//div[@class='entries']/a[2]"
        ).click()

        try:
            # 等待，直到登录框加载
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((
                    By.XPATH,
                    "//div[@class='form-wrapper']"
                )))
        except Exception as _:
            print('登陆页面加载超时！')
        else:
            self.driver.find_element_by_xpath(
                "//input[@name='mobileOrEmail']"
                ).send_keys(self.data['email'])
            self.driver.find_element_by_xpath(
                '//input[@name="password"]'
                ).send_keys(self.data['password'])
            self.driver.find_element_by_xpath(
                "//button[contains(@class, 'submit')]"
                ).click()

            try:
                # 由于selenium没法获取状态码
                # 考虑通过目标页面是否加载来判断是否登陆成功
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((
                        By.XPATH,
                        "//a[contains(@class, 'Nav-sc-VyK8c-1')]"
                    )))  # 等待“最近使用”显示
            except Exception as _:
                print('登陆失败')
            else:
                print('登陆成功')

    def close(self):
        self.driver.close()
        self.driver.quit()


if __name__ == '__main__':
    email = input('请输入邮箱：') or 'underfined'
    mobile = input('请输入手机号：') or '+86undefined'
    psw = input('请输入密码：')
    
    data = {
        'email': email,
        'mobile': mobile,
        'password': psw
    }
    print(data)
    shimo = ShiMo(data)
    shimo.login()
    shimo.close()