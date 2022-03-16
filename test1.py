# import pytest
import time
# import json
import re
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support import expected_conditions
# from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import selenium.webdriver.support.ui as ui

chrome_opt = Options()  # 创建参数设置对象.
chrome_opt.add_argument('--headless')  # 无界面化.
chrome_opt.add_argument('--disable-gpu')  # 配合上面的无界面化.
chrome_opt.add_argument('--window-size=1920,1020')  # 设置窗口大小, 窗口大小会有影响.


class Test1():
    def setup_method(self, method):
        self.driver = webdriver.Chrome()
        self.vars = {}

    def teardown_method(self, method):
        self.driver.quit()

    def wait_for_window(self, timeout=2):
        time.sleep(round(timeout / 1000))
        wh_now = self.driver.window_handles
        wh_then = self.vars["window_handles"]
        if len(wh_now) > len(wh_then):
            return set(wh_now).difference(set(wh_then)).pop()

    def test_1(self, name):
        # Test name: 1
        # Step # | name | target | value
        # 1 | open | / |
        self.driver.get("https://appgallery.huawei.com/")
        # 2 | setWindowSize | 1920x1020 |
        self.driver.set_window_size(1920, 1020)
        # 3 | click | css=input |
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, "input").click()
        # 4 | type | css=input | name
        self.driver.find_element(By.CSS_SELECTOR, "input").send_keys(name)
        # 5 | sendKeys | css=input | ${KEY_ENTER}
        self.driver.find_element(By.CSS_SELECTOR,
                                 "input").send_keys(Keys.ENTER)
        # 6 | click | css=div:nth-child(1) > .ser > .tem:nth-child(1) p:nth-child(1) |
        time.sleep(1)
        self.driver.find_element(
            By.CSS_SELECTOR,
            "div:nth-child(1) > .ser > .tem:nth-child(1) p:nth-child(1)"
        ).click()
        # 7 | click | css=.mouse_pointer:nth-child(3) |
        self.vars["window_handles"] = self.driver.window_handles
        # 8 | selectWindow | handle=${win9804} |
        # time.sleep(5)
        try:
            wait = ui.WebDriverWait(self.driver, 5)
            wait.until(lambda driver: self.driver.find_element_by_xpath(
                "/html//div/div[2]/div/div[3]/div[7]/div/div[2]/div[2]/div[3]")
                       )  # 这里这句必须加
        except:
            self.driver.delete_all_cookies()
            return self.test_1(name)

        element = self.driver.find_element_by_xpath(
            "/html//div/div[2]/div/div[3]/div[7]/div/div[2]/div[2]/div[3]")
        self.driver.execute_script("arguments[0].click();", element)
        # self.driver.find_element(By.CSS_SELECTOR, ".mouse_pointer:nth-child(3)").click()
        self.vars["win9804"] = self.wait_for_window(2000)
        self.driver.switch_to.window(self.vars["win9804"])
        currentPageUrl = self.driver.current_url
        html_sourcecode = self.driver.page_source
        s = html_sourcecode
        soup = BeautifulSoup(s, 'html.parser')
        [script.extract() for script in soup.findAll('script')]
        [style.extract() for style in soup.findAll('style')]
        soup.prettify()
        reg1 = re.compile("<[^>]*>")
        content = reg1.sub('', soup.prettify())  # 有很多空格，换行符，有一定格式
        # [x.extract() for x in soup.find_all('script')]
        # content = content.replace("\n+", "")
        file_handle = open(
            str(name) + '.txt',
            mode='w',
            encoding="utf-8")
        for line in content.splitlines():
            if line in ['\n', '\r\n'] or line.strip() == "":
                pass
            else:
                line = line.strip()
                print(line)
                file_handle.write(line + '\n')
        file_handle.close()
        return currentPageUrl
