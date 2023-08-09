from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# from webdriver_manager.firefox import GeckoDriverManager
# from selenium.webdriver import FirefoxProfile
# from selenium.webdriver.firefox.options import Options

# FireFox
# profile_path = r'C:\Users\Owner\AppData\Roaming\Mozilla\Firefox\Profiles\0007gipx.Default User'
# profile_path = r'C:\Users\Owner\AppData\Local\Mozilla\Firefox\Profiles\0007gipx.Default User'
# profile = webdriver.FirefoxProfile(profile_path)
# driver = webdriver.Firefox(firefox_profile=profile)

# url = "https://with.is/messages"
# url = "https://scraping-for-beginner.herokuapp.com/login_page"

# url = "https://feedly.com/i/label/feedly.history"
url = "https://feedly.com/i/collection/content/user/edf3192f-0b80-4568-9b14-0363076afde0/category/global.all"
dataset = []
items = []

class Config:
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # GCP鍵
    json = 'try-selenium-pro-b5215b62b8f8.json'

    #書き込み先のスプレッドシートキー
    SPREADSHEET_KEY = '10TIyDRbwX5oZI066yXx3eM4xe-a0g4KqYIRhxn8mCjk'

    # profile_path = r"C:\Users\Owner\AppData\Local\Google\Chrome\User Data"
    # デスクトップ
    # profile_path = r"C:\Users\Owner\Documents\try_py\chrome_profile"
    # ラックトップ
    profile_path = r"C:\Users\sekai\OneDrive\ドキュメント\try_py\chrome_profile"
    account_name = "login_seleninium"

class ChromeBrowzer:
    options = Options()
    options.add_argument('--no-sandbox')
    options.add_argument('--user-data-dir=' + Config.profile_path)
    options.add_argument(f'--profile-directory={Config.account_name}')
    options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option('detach', True)
    browser = webdriver.Chrome(options=options)
    browser.get(url)

credentials = ServiceAccountCredentials.from_json_keyfile_name(Config.json, Config.scope)
gc = gspread.authorize(credentials)

def getVal_with():
    global items
    elems = browser.find_elements(By.CLASS_NAME, 'topic_nickname')
    print('-getval-')
    items = []
    for elem in elems:
        print(elem.text)
        items.append(elem.text)

def getVal_feedly():
    global dataset
    elemTitles = []
    elemUrls = []
    elem_EntryList__chunks = browser.find_elements(By.CLASS_NAME, 'EntryList__chunk')
    print('EntryList__chunks: ', len(elem_EntryList__chunks))
    for elem_EntryList__chunk in elem_EntryList__chunks:
        EntryTitleLinks = elem_EntryList__chunk.find_elements(By.CLASS_NAME,"EntryTitleLink")
        print('EntryTitleLinks: ', len(EntryTitleLinks))
        for EntryTitleLink in EntryTitleLinks:
            print(EntryTitleLink.text)
            print(EntryTitleLink.get_attribute('href'))
            elemTitles.append(EntryTitleLink.text)
            elemUrls.append(EntryTitleLink.get_attribute('href'))
    dataset.append(elemTitles)
    dataset.append(elemUrls)
    
def login_imanishi():
    elem_username = browser.find_element(By.ID, 'username')
    elem_password = browser.find_element(By.ID, 'password')
    elem_login_btn = browser.find_element(By.ID, 'login-btn')
    elem_username.send_keys('imanishi')
    elem_password.send_keys('kohei')
    elem_login_btn.click()

def getVal_imanishi():
    elems = browser.find_elements(By.TAG_NAME, 'td')
    items = []
    print('-getval-')
    for elem in elems:
        # print(elem.text)
        items.append(elem.text)

def rightGspread(dataset):
    #共有設定したスプレッドシートの1枚目のシートを開く
    worksheet = gc.open_by_key(Config.SPREADSHEET_KEY).sheet1
    
    # worksheet.append_row(items)
    # for num in range(len(items)+1):
   
    count = 1
    for (title, data) in zip(dataset[0], dataset[1]):
        cell = worksheet.update('A' + str(count), title)
        cell = worksheet.update('B' + str(count), data)
        count += 1
        if count <= 5:
            break
        
def openNewTab(url):
    browser.execute_script(f"window.open('{url}');")
    
browser = ChromeBrowzer.browser

# login_imanishi(browser)
# items = getVal_imanishi(browser)
# getVal_with(browser)

sleep(5)

getVal_feedly()
rightGspread(dataset)

print('取得数: ', len(dataset[0]))
print(dataset[0][0])
openNewTab(dataset[1][0])

# browser.quit()