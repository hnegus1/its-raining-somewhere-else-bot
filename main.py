import json
import requests
import random
from dotenv import load_dotenv
import os
from blueskysocial import Client, Post, WebCard
import time
load_dotenv()

def run():
    bsky_user = os.environ.get("BSKY_USER")
    bsky_pass = os.environ.get("BSKY_PASS")

    client = Client()
    client.authenticate(bsky_user, bsky_pass)

    data = None
    with open('data/city.list.json', encoding='utf-8') as cities:
        data = json.load(cities)

    countries_list = None
    with open('data/countries.json', encoding='utf-8') as countries:
        countries_list = json.load(countries)

    while True:
        def get_random_cities():
            cities = []
            for x in range(20):
                cities.append(data[random.randrange(0, len(data) - 1)]) 

            return cities


        def get_potential_rainy_cities(cities):      
            url = f'https://api.open-meteo.com/v1/forecast?latitude={",".join(map(lambda city: str(city["coord"]["lat"]), cities))}&longitude={",".join(map(lambda city: str(city["coord"]["lon"]), cities))}&current=rain&forecast_days=0'
            response = requests.get(url)
            return response.json()

        def is_it_raining(weather):
            return weather["rain"] > 0.00
        
        
        found_potential_rainy_cities = False
        times_looked = 0
        where_its_raining = None
        while found_potential_rainy_cities is False:
            if times_looked >= 3:
                print("cannot find any rainy cities... will look again.")
                time.sleep(60)#To not annoy the API
                times_looked = 0
            
            random_cities = get_random_cities()
            weather_result = get_potential_rainy_cities(random_cities)

            for i, r in enumerate(weather_result):
                random_cities[i]["rain"] = r["current"]["rain"]

            where_its_raining = list(filter(is_it_raining, random_cities))
            times_looked += 1
            if len(where_its_raining) > 0:
                found_potential_rainy_cities = True

        rainy_city = where_its_raining[0]

        post = f'It\'s raining in {rainy_city["name"]}, {countries_list[rainy_city["country"]]}.'
        bskypost = Post(post, with_attachments=WebCard('https://www.youtube.com/watch?v=KtC-pl9P3kE'))
        client.post(bskypost)
        time.sleep(3600)



if __name__ == "__main__":
   run()