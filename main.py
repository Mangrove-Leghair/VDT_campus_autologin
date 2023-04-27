import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class Login:
    def __init__(self):
        self.username = os.getenv("USERNAME_ENV_VAR")
        self.password = os.getenv("PASSWORD_ENV_VAR")

        if not (self.username and self.password):
            self.get_credentials()

        self.options = Options()
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptInsecureCerts'] = True
        self.driver = webdriver.Chrome(executable_path="C:\Program Files\Auto_login\chromedriver.exe",desired_capabilities=capabilities, options=self.options)
        self.driver.get("https://172.16.0.1:8090/")

        self.login()

    def get_credentials(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        os.environ["USERNAME_ENV_VAR"] = self.username
        os.environ["PASSWORD_ENV_VAR"] = self.password

    def login(self):
        time.sleep(3)
        username_field = self.driver.find_element(By.NAME, "username")
        password_field = self.driver.find_element(By.NAME, "password")
        username_field.send_keys(self.username)
        password_field.send_keys(self.password)
        login_button = self.driver.find_element(By.ID, "loginbutton")
        login_button.click()

        while True:
            try:
                time.sleep(10)
                self.driver.title
            except:
                break

        self.driver.quit()


'''pyinstaller --onefile --name=AutoLogin --icon=key.ico Test.py'''

if __name__ == "__main__":
    login = Login()
    print(f"Welcome, {login.username}!")
