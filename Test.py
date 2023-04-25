import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

import win32serviceutil
import win32service
import win32event
import servicemanager

class Login(win32serviceutil.ServiceFramework):
    _svc_name_ = "LoginService"
    _svc_display_name_ = "Login Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)

        self.username = os.getenv("USERNAME_ENV_VAR")
        self.password = os.getenv("PASSWORD_ENV_VAR")

        if not (self.username and self.password):
            self.get_credentials()

        self.options = Options()
        capabilities = DesiredCapabilities.CHROME.copy()
        capabilities['acceptInsecureCerts'] = True
        self.driver = webdriver.Chrome(desired_capabilities=capabilities, options=self.options)
        self.driver.get("https://172.16.0.1:8090/")

    def get_credentials(self):
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")
        os.environ["USERNAME_ENV_VAR"] = self.username
        os.environ["PASSWORD_ENV_VAR"] = self.password

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.login()

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

if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(Login)