import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
import time

class MyService(win32serviceutil.ServiceFramework):
    _svc_name_ = "MyService"
    _svc_display_name_ = "My Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.stop_event)

    def SvcDoRun(self):
        # set up the webdriver with the desired browser (e.g. Chrome)
        caps = DesiredCapabilities().CHROME
        caps['acceptInsecureCerts'] = True
        driver = webdriver.Chrome(desired_capabilities=caps)

        # navigate to the login page
        driver.get("https://172.16.0.1:8090/")

        # wait for the page to fully load
        time.sleep(3)

        # find the username and password fields and fill them in
        username_field = driver.find_element(by=By.NAME, value="username")
        password_field = driver.find_element(by=By.NAME, value="password")
        username_field.send_keys("shanti.krishnan")
        password_field.send_keys("shanti@123")

        # click the Login button
        login_button = driver.find_element(by=By.ID, value="loginbutton")
        login_button.click()

        # keep the browser window open until the service is stopped
        while True:
            try:
                time.sleep(10)  # wait for 10 seconds before checking if the browser is still open
                driver.title  # try to access the browser title to check if the browser is still open
            except:
                break  # exit the loop if the browser is closed

        # close the browser window
        driver.quit()

if __name__ == '__main__':
    win32serviceutil.HandleCommandLine(MyService)