import requests
from bs4 import BeautifulSoup
first = 192
url = 'https://slovarozhegova.ru/letter.php?charkod='
all_words = []
for i in range(first,224):
    print(i)
    data = requests.get(url+str(i))
    print(url+str(i))
    soup = BeautifulSoup(data.text,'html.parser')
    all = soup.find_all('strong')
    print(soup)
    all_words.extend([k.text for k in all if len(k.text) >= 3])
    print(all_words)
print(all_words)
