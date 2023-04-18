from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import os

USERNAME_ENV_VAR = "USERNAME_ENV_VAR"
PASSWORD_ENV_VAR = "PASSWORD_ENV_VAR"

# Try to read the credentials from environment variables
username = os.getenv(USERNAME_ENV_VAR)
password = os.getenv(PASSWORD_ENV_VAR)

if not (username and password):
    # If the environment variables are not set, prompt the user for credentials
    username = input("Enter your username for this time: ")
    password = input("Enter your password for this time: ")
    # Set the environment variables for the credentials
    os.system(f'setx USERNAME_ENV_VAR "{username}"')
    os.system(f'setx PASSWORD_ENV_VAR "{password}"')

# Use the credentials
print(f"Welcome, {username}!")

# set up the webdriver with the desired browser (e.g. Chrome)
caps = DesiredCapabilities().CHROME
caps['acceptInsecureCerts'] = True
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# navigate to the login page
driver.get("https://172.16.0.1:8090/")

# wait for the page to fully load
time.sleep(3)

# find the username and password fields and fill them in
username_field = driver.find_element(by=By.NAME, value="username")
password_field = driver.find_element(by=By.NAME, value="password")
username_field.send_keys(f'{username}')
password_field.send_keys(f'{password}')

# click the Login button
login_button = driver.find_element(by=By.ID, value="loginbutton")
login_button.click()

# keep the browser window open until the user closes it
while True:
    try:
        time.sleep(10)  # wait for 10 seconds before checking if the browser is still open
        driver.title  # try to access the browser title to check if the browser is still open
    except:
        break  # exit the loop if the browser is closed

# close the browser window
driver.quit()
