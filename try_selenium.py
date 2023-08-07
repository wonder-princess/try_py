from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver import FirefoxProfile
# from selenium.webdriver.firefox.options import Options

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# GCP鍵
json = 'try-selenium-pro-b5215b62b8f8.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
gc = gspread.authorize(credentials)

#書き込み先のスプレッドシートキー
SPREADSHEET_KEY = '10TIyDRbwX5oZI066yXx3eM4xe-a0g4KqYIRhxn8mCjk'



# FireFox
# profile_path = r'C:\Users\Owner\AppData\Roaming\Mozilla\Firefox\Profiles\0007gipx.Default User'
# profile_path = r'C:\Users\Owner\AppData\Local\Mozilla\Firefox\Profiles\0007gipx.Default User'
# profile = webdriver.FirefoxProfile(profile_path)
# driver = webdriver.Firefox(firefox_profile=profile)

url = "https://with.is/messages"
# url = "https://scraping-for-beginner.herokuapp.com/login_page"
# profile_path = r"C:\Users\Owner\AppData\Local\Google\Chrome\User Data"


profile_path = r"C:\Users\Owner\Documents\try_py\chrome_profile"
account_name = "login_seleninium"

# Chrome
def openBrowser():
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--user-data-dir=' + profile_path)
    options.add_argument(f'--profile-directory={account_name}')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    return browser

def getVal(browser):
    elems = browser.find_elements(By.CLASS_NAME, 'topic_nickname')
    
    print('-getval-')
    
    for elem in elems:
        print(elem.text)
        
def rightVal():
    elems = browser.find_elements(By.CLASS_NAME, 'topic_nickname')
    
    

def login_imanishi(browser):
    elem_username = browser.find_element(By.ID, 'username')
    elem_password = browser.find_element(By.ID, 'password')
    elem_login_btn = browser.find_element(By.ID, 'login-btn')
    
    elem_username.send_keys('imanishi')
    elem_password.send_keys('kohei')
    elem_login_btn.click()

def getVal_imanishi(browser):
    val = browser.find_element(By.ID, 'name')
    print(val.text)

    
    
browser = openBrowser()

# login_imanishi(browser)
# getVal_imanishi(browser)

getVal(browser)

browser.quit()

#共有設定したスプレッドシートの1枚目のシートを開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

#書き込み用の文字列を作成
items = ['Hello', 'World']
# シートへ文字列を追加
worksheet.append_row(items)
