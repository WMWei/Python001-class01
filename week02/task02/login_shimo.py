from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# driver 初始化
chrome_op = webdriver.ChromeOptions()
chrome_op.add_argument('--headless')
chrome_op.add_argument('--disable-gpu')
driver = webdriver.Chrome(options=chrome_op)

home_url = 'https://shimo.im/welcome'
data = {
        'email': 'xxx@xxx.com',
        'mobile': '+86undefined',
        'password': 'xxxxxxxx'
}

driver.get(home_url)
driver.find_element_by_xpath('//button[@class="login-button btn_hover_style_8"]').click()
try:
    WebDriverWait(driver, 30).until(EC.presence_of_element_located(
        (By.XPATH, "//div[@class='form-wrapper']")
        )
    )
except Exception as _:
    print('超时！')

driver.find_element_by_xpath('//input[@type="text"]').send_keys(data['email'])
driver.find_element_by_xpath('//input[@type="password"]').send_keys(data['password'])
driver.find_element_by_xpath('//button[@class="sm-button submit sc-1n784rm-0 bcuuIb"]').click()

print(driver.page_source)
