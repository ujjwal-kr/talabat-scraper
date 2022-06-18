import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

sample_data = [
    "https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308",
    "https://www.talabat.com/uae/restaurant/645430/pasta-della-nona-jlt-jumeirah-lakes-towers?aid=1308",
    "https://www.talabat.com/uae/restaurant/50445/pizzaro-marina-3?aid=1308",
    "https://www.talabat.com/uae/restaurant/605052/the-pasta-guyz-dubai-marina?aid=1308",
    "https://www.talabat.com/uae/restaurant/621796/pizza-di-rocco-jumeirah-lakes-towers--jlt?aid=1308",
    "https://www.talabat.com/uae/restaurant/628551/shawarmatacjumeirah-1?aid=1280",
    "https://www.talabat.com/uae/restaurant/26820/mcdonalds-jumeirah1?aid=1302",
    "https://www.talabat.com/uae/restaurant/664597/tostatto-cafe?aid=1486",
    "https://www.talabat.com/uae/restaurant/32444/wingstop-mirdif?aid=1198",
    "https://www.talabat.com/uae/restaurant/606319/chickzoneal-raffa?aid=1187"
]


class Scraper:
    def __init__(self, sample_data):
        self.urls = sample_data
        self.restaurant_data = []

    def scrape(self):
        print("Please Wait...")
        for url in self.urls:
            resp = requests.get(url)
            if resp.status_code != 200:
                print(f"URL Not Found!: {url}")
                break
            soup = BeautifulSoup(resp.content, 'html.parser')
            json_dict = json.loads(soup.find('script', {'id': '__NEXT_DATA__'}).contents[0])[
                'props']['pageProps']['initialMenuState']
            restaurant_name = json_dict['restaurant']['name']
            restaurant_logo = json_dict['restaurant']['logo']
            latitude = json_dict['restaurant']['latitude']
            longitude = json_dict['restaurant']['longitude']
            cuisine_tags = json_dict['restaurant']['cuisineString'].split(',')
            menu_items = []
            for item in json_dict['menuData']['items']:
                menu_item = {}
                menu_item['item_name'] = item['name']
                menu_item['item_description'] = item['description']
                menu_item['item_price'] = item['price']
                menu_item['items_image'] = item['image']
                menu_items.append(menu_item)
            self.restaurant_data.append({'restaurant_name': restaurant_name, 'restaurant_logo': restaurant_logo, 
                                        'latitude': latitude, 'longitude': longitude, 'cuisine_tags': cuisine_tags, 'menu_items': menu_items})
        self.pretty_print()
        self.export_to_csv()

    def pretty_print(self):
        df = pd.DataFrame(self.restaurant_data)
        print(df)

    def export_to_csv(self):
        df = pd.DataFrame(self.restaurant_data)
        df.to_csv("data.csv", sep="\t", encoding="utf-8")


data = Scraper(sample_data).scrape()
