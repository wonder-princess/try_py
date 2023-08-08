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

# FireFox
# profile_path = r'C:\Users\Owner\AppData\Roaming\Mozilla\Firefox\Profiles\0007gipx.Default User'
# profile_path = r'C:\Users\Owner\AppData\Local\Mozilla\Firefox\Profiles\0007gipx.Default User'
# profile = webdriver.FirefoxProfile(profile_path)
# driver = webdriver.Firefox(firefox_profile=profile)

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# GCP鍵
json = 'try-selenium-pro-b5215b62b8f8.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)
gc = gspread.authorize(credentials)

#書き込み先のスプレッドシートキー
SPREADSHEET_KEY = '10TIyDRbwX5oZI066yXx3eM4xe-a0g4KqYIRhxn8mCjk'


# url = "https://with.is/messages"
# url = "https://scraping-for-beginner.herokuapp.com/login_page"
url = "https://feedly.com/i/collection/content/user/edf3192f-0b80-4568-9b14-0363076afde0/category/global.all"


# profile_path = r"C:\Users\Owner\AppData\Local\Google\Chrome\User Data"
# デスクトップ
# profile_path = r"C:\Users\Owner\Documents\try_py\chrome_profile"
# ラックトップ
profile_path = r"C:\Users\sekai\OneDrive\ドキュメント\try_py\chrome_profile"
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

def getVal_with(browser):
    elems = browser.find_elements(By.CLASS_NAME, 'topic_nickname')
    print('-getval-')
    items = []
    for elem in elems:
        print(elem.text)
        items.append(elem.text)
    return items

def getVal_feedly(browser):
    elemTitles = []
    elemUrls = []
    elem_EntryList__chunks = browser.find_elements(By.CLASS_NAME, 'EntryList__chunk')
    for elem_EntryList__chunk in elem_EntryList__chunks:
        EntryTitleLinks = elem_EntryList__chunk.find_elements(By.CLASS_NAME,"EntryTitleLink")
        for EntryTitleLink in EntryTitleLinks:
            print(EntryTitleLink.text)
            print(EntryTitleLink.get_attribute('href'))
            elemTitles.append(EntryTitleLink.text)
            elemUrls.append(EntryTitleLink.get_attribute('href'))
    
    items = [elemTitles, elemUrls]
    return items
    
def login_imanishi(browser):
    elem_username = browser.find_element(By.ID, 'username')
    elem_password = browser.find_element(By.ID, 'password')
    elem_login_btn = browser.find_element(By.ID, 'login-btn')
    
    elem_username.send_keys('imanishi')
    elem_password.send_keys('kohei')
    elem_login_btn.click()

def getVal_imanishi(browser):
    elems = browser.find_elements(By.TAG_NAME, 'td')
    items = []
    print('-getval-')
    for elem in elems:
        # print(elem.text)
        items.append(elem.text)
    return items

def rightGspread(items):
    #共有設定したスプレッドシートの1枚目のシートを開く
    worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1
    
    # worksheet.append_row(items)
    # for num in range(len(items)+1):
   
    count = 1
    for (title, data) in zip(items[0], items[1]):
        cell = worksheet.update('A' + str(count), title)
        cell = worksheet.update('B' + str(count), data)
        
        count += 1
        
browser = openBrowser()

# login_imanishi(browser)
# items = getVal_imanishi(browser)
# getVal_with(browser)

sleep(10)

items = getVal_feedly(browser)
rightGspread(items)

browser.quit()