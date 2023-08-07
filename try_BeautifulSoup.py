import requests
from bs4 import BeautifulSoup

res = requests.get('https://with.is/messages')
soup = BeautifulSoup(res.text, 'html.parser')

usernames = soup.find('div', class_='topic_nickname text-ellipsis')
# print(x.string for x in usernames)
print(usernames)