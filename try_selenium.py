from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from time import sleep
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import os
import datetime
import pyautogui

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
url = "https://with.is/campaigns/173/users?page=78&paging_order=2"
# dataset = pd.DataFrame(index=[], columns=[])

class Config:
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # GCP鍵
    json = 'try-selenium-pro-b5215b62b8f8.json'

    #書き込み先のスプレッドシートキー
    SPREADSHEET_KEY = '10TIyDRbwX5oZI066yXx3eM4xe-a0g4KqYIRhxn8mCjk'

    # profile_path = r"C:\Users\Owner\AppData\Local\Google\Chrome\User Data"
    # デスクトップ
    profile_path = r"C:\Users\Owner\Documents\try_py\chrome_profile"
    # ラックトップ
    # profile_path = r"C:\Users\sekai\OneDrive\ドキュメント\try_py\chrome_profile"
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
    browser.set_window_size(1280,800)
    



dataFrame = pd.DataFrame(index=[])
dataset = []
items = []
browser = ChromeBrowzer.browser
credentials = ServiceAccountCredentials.from_json_keyfile_name(Config.json, Config.scope)
gc = gspread.authorize(credentials)

def getVal_with_userUrl_campaigns():
    global dataFrame
    dataFrame = pd.DataFrame(columns=['userid', 'URL'])
    elem_grid = browser.find_element(By.CLASS_NAME, 'grid')
    elem_users = elem_grid.find_elements(By.CLASS_NAME, 'user-card-small')
    for elem_user in elem_users:
        userid = elem_user.get_attribute('data-user-id')
        if userid == '':
            continue
        record = pd.Series([userid, f"https://with.is/users/{userid}"], index = dataFrame.columns)
        dataFrame = pd.concat([dataFrame, pd.DataFrame([record])], ignore_index=True)

def getVal_with_userUrl_campaigns_():
    global dataFrame
    dataFrame = pd.DataFrame(columns=['userid', 'URL'])
    elem_grid = browser.find_element(By.CLASS_NAME, 'grid')
    elem_users = elem_grid.find_elements(By.CLASS_NAME, 'user-card-small')
    for elem_user in elem_users:
        userid = elem_user.get_attribute('data-user-id')
        if userid == '':
            continue
        get_with_userProfileData(f"https://with.is/users/{userid}")

def get_with_userProfileData(userUrl):
    global dataFrame
    browser.execute_script(f"window.open('{url}');")
    userNmae = browser.find_element(By.CLASS_NAME, 'profile_main-nickname').text
    userAgeAddress = browser.find_element(By.CLASS_NAME, 'profile_main-age-address').text

    

def getVal_feedly():
    global dataFrame
    dataFrame = pd.DataFrame(columns=['タイトル', 'URL', 'ソース', '日付'])
    
    elem_EntryList__chunks = browser.find_elements(By.CLASS_NAME, 'EntryList__chunk')
    print('EntryList__chunks: ', len(elem_EntryList__chunks))
    for elem_EntryList__chunk in elem_EntryList__chunks:
        elem_articlTitles = elem_EntryList__chunk.find_elements(By.CLASS_NAME,"TitleOnlyLayout--density-cozy")
        print('articlTitles: ', len(elem_articlTitles))
        for elem_articlTitle in elem_articlTitles:
            
            articlTitleText = elem_articlTitle.find_element(By.CLASS_NAME,"EntryTitleLink").text
            articlTitleLink = elem_articlTitle.find_element(By.CLASS_NAME,"EntryTitleLink").get_attribute('href')
            articlSauce = elem_articlTitle.find_element(By.CLASS_NAME,"EntryMetadataSource")
            articlDate = elem_articlTitle.find_element(By.XPATH,"//span[@class='ago']").get_attribute('title')
            
            record = pd.Series([articlTitleText, articlTitleLink, articlSauce.text, articlDate], index = dataFrame.columns)
            dataFrame = pd.concat([dataFrame, pd.DataFrame([record])], ignore_index=True)
    
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

def outputGspread(dataset):
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
        
def outputExcel():
    currentDir = os.getcwd()
    nowtime =  datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S")

    df = pd.DataFrame(dataset, columns=['タイトル', 'URL'])
    df.to_excel(f"{currentDir}/{nowtime}.xlsx")
    
def outputCsv():
    currentDir = os.getcwd()
    nowtime =  datetime.datetime.now().strftime("%y-%m-%d %H-%M-%S")
    # fileName = "output.csv"
    
    df = pd.DataFrame(dataFrame)
    df.to_csv(f"{currentDir}/{nowtime}.csv", index=False)
            
def openNewTab(url):
    browser.execute_script(f"window.open('{url}');")
    
def scrollWindow():
    # browser.find_element(By.TAG_NAME, 'body').click()
    
    # pyautogui.scroll(-800)
    
    # pyautogui.hold('pagedown', presses=60)
    pyautogui.keyDown('pagedown')
    # print('push')
    # sleep(10)
    # pyautogui.keyUp('pagedown', interval=5)
    
    # nowItems = browser.execute_script("return document.getElementsByClassName('ListView__ItemContainer-sc-1veaxzq-1')")
    # browser.execute_script("document.getElementsByClassName('ListView__ItemContainer-sc-1veaxzq-1')[%d].scrollIntoView(true)" % int(len(nowItems)-1))

def scrollWindow_():
    sleep(5)
    #ブラウザのウインドウ高を取得する
    win_height = browser.execute_script("return window.innerHeight")
    print(f"ブラウザの高さ{win_height}")
    
    #スクロール開始位置の初期値（ページの先頭からスクロールを開始する）
    last_top = 1
    
    #ページの最下部までスクロールする無限ループ
    while True:
        #スクロール前のページの高さを取得
        last_height = browser.execute_script("return document.body.scrollHeight")
        
        #スクロール開始位置を設定
        top = last_top
        print(f"スクロール開始位置{top}")
        
        #ページ最下部まで、徐々にスクロールしていく
        while top < last_height:
            top += int(win_height * 0.8)
            browser.execute_script(f"window.scrollTo(0, {top})")
            sleep(0.1)

        #１秒待って、スクロール後のページの高さを取得する
        sleep(1)
        new_last_height = browser.execute_script("return document.body.scrollHeight")
        
        #スクロール前後でページの高さに変化がなくなったら無限スクロール終了とみなしてループを抜ける
        if last_height == new_last_height or int(last_top) > 1000000:
            print("スクロール終了")
            break
        
        #次のループのスクロール開始位置を設定
        last_top = last_height
    
# login_imanishi(browser)
# items = getVal_imanishi(browser)


scrollWindow_()
getVal_with_userUrl_campaigns()

# getVal_feedly()
# rightGspread(dataset)

# openNewTab(dataset[1][0])

# outputExcel()

outputCsv()

browser.quit()