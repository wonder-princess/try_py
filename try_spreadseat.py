import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

#ダウンロードしたjsonファイルをドライブにアップデートした際のパス
json = 'try-selenium-pro-b5215b62b8f8.json'

credentials = ServiceAccountCredentials.from_json_keyfile_name(json, scope)

gc = gspread.authorize(credentials)

#書き込み先のスプレッドシートキーを追加
SPREADSHEET_KEY = '10TIyDRbwX5oZI066yXx3eM4xe-a0g4KqYIRhxn8mCjk'

#共有設定したスプレッドシートの1枚目のシートを開く
worksheet = gc.open_by_key(SPREADSHEET_KEY).sheet1

#書き込み用の文字列を作成
items = ['Hello', 'World']
# シートへ文字列を追加
worksheet.append_row(items)