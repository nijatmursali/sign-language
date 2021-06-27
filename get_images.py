import bs4
import requests
from PIL import Image

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i','j', 'k', 'l','m', 'n', 'o','p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

for letter in letters:
    url = f'https://www.babysignlanguage.com/dictionary-letter/?letter={letter}'

    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, 'html.parser')

    content = str(soup.find_all('div', {"class": "single-letter-card"}))

    soup1 = bs4.BeautifulSoup(content, 'html.parser')

    hrefList = []

    for a in soup1.find_all('a', href=True):
        hrefList.append(a['href'])

    imageList = []
    for href in hrefList:
        res = requests.get(href)
        soup2 = bs4.BeautifulSoup(res.text, 'html.parser')
        cnt = str(soup2.find_all('div', {"class": "hero-right"}))
        soup3 = bs4.BeautifulSoup(cnt, 'html.parser')
        for img in soup3.find_all('img'):
            imageInfo = img['src'].split('/')
            imageInfo = imageInfo[-1].split('.')
            print(img['src'])
            image = Image.open(requests.get(f"https:{img['src']}?", stream = True).raw)
            image = image.resize((512, 512), Image.ANTIALIAS)
            image.save(f'./new/{imageInfo[0]}.png')