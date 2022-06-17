import requests
from bs4 import BeautifulSoup
import json

sample_data = [
    "https://www.talabat.com/uae/restaurant/621133/ginos-deli-jlt?aid=1308",
    "https://www.talabat.com/uae/restaurant/645430/pasta-della-nona-jlt-jumeirah-lakes-towers?aid=1308",
    "https://www.talabat.com/uae/restaurant/50445/pizzaro-marina-3?aid=1308",
    "https://www.talabat.com/uae/restaurant/605052/the-pasta-guyz-dubai-marina?aid=1308",
    "https://www.talabat.com/uae/restaurant/621796/pizza-di-rocco-jumeirah-lakes-towers--jlt?aid=1308"
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
            menu_items = {}
            for item in json_dict['menuData']['items']:
                menu_items['item_name'] = item['name']
                menu_items['item_description'] = item['description']
                menu_items['item_price'] = item['price']
                menu_items['items_image'] = item['image']
            self.restaurant_data.append([{'restaurant_name': restaurant_name}, {'restaurant_logo': restaurant_logo}, {
                                        'latitude': latitude}, {'longitude': longitude}, {'cuisine_tags': cuisine_tags}, {'menu_items': menu_items}])
        self.pretty_print()

    def pretty_print(self):
        print(self.restaurant_data)


data = Scraper(sample_data).scrape()
