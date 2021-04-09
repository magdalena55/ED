from bs4 import BeautifulSoup
from requests import get

# sciezka do ofert:
for i in range(1, 120):
    URL = 'https://gethome.pl/mieszkania/do-wynajecia/krakow/?page=i'


    def parse_price(price):
        return float(price.replace(' ', '').replace('zł/miesiąc', ''))


    def parse_info(info):
        return info.replace('pokoje', '').replace('pokój', '').replace('m2', '')


    def parse_floor(floor):
        return floor.replace('Cena za m2', '').replace('Piętro', '').replace('zł', '').replace('Dostępne', '').replace('Dodatkowa', '')


    # pobieranie zawartości strony
    page = get(URL)

    # do konstruktora obiektu bs przekazujemy kontent
    bs = BeautifulSoup(page.content, 'html.parser')

    # przechodzimy po wszystkich ofertach
    for offer in bs.find_all('div', class_='css-1our9ed-offerBoxWrapper'):
        location = offer.find('p', class_='css-unl6d4-PropertyLocation-ellipsis e1es8y4n4').get_text().strip().split(',')[1]
        price = parse_price(offer.find('p', class_='css-pce4ym-Price eeuzmg10').get_text().strip())
        rooms = parse_info(offer.find('div', class_='css-jg9o52-Flex e8aa8cc0').get_text().strip()).split(' ')[0]
        area = parse_info(offer.find('div', class_='css-jg9o52-Flex e8aa8cc0').get_text().strip()).split(' ')[1]

        link = offer.find('a')
        page2 = get('https://gethome.pl'+link['href'])
        bs2 = BeautifulSoup(page2.content, 'html.parser')
        floor = parse_floor(bs2.find('div', class_='css-1id7vsr-FeaturesList e1kihjfm0').get_text()).split(' ')[1]
        #print(floor)
        print(location, price, rooms, area, floor)
