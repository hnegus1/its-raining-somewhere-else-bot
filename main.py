import json
import requests
import random
from dotenv import load_dotenv
import os
import asyncio
import tweepy
import time
load_dotenv()

def mastodon(toot):
    access_token = os.environ.get("MASTODON_ACCESS_TOKEN")

    post_url = f'https://mastodon.videogamesarebad.co.uk/api/v1/statuses'
    post_response = requests.post(
        post_url, 
        headers={"Authorization": f"Bearer {access_token}"}, 
        data={"status": toot}
    )


def run():
    weather_key = os.environ.get("WEATHER_KEY")
    twitter_consumer_key = os.environ.get("TWITTER_KEY")
    twitter_consumer_secret = os.environ.get("TWITTER_SECRET")
    twitter_access_token = os.environ.get("TWITTER_ACCESS_TOKEN")
    twitter_access_token_secret = os.environ.get("TWITTER_ACCESS_TOKEN_SECRET")

    auth = tweepy.OAuthHandler(twitter_consumer_key, twitter_consumer_secret)
    auth.set_access_token(twitter_access_token, twitter_access_token_secret)

    api = tweepy.API(auth)

    data = None
    with open('data/city.list.json', encoding='utf-8') as cities:
        data = json.load(cities)

    countries_list = None
    with open('data/countries.json', encoding='utf-8') as countries:
        countries_list = json.load(countries)

    while True:
        def get_potential_rainy_cities():
            cities = []
            for x in range(20):
                cities.append(data[random.randrange(0, len(data) - 1)]) 

            url = f'http://api.openweathermap.org/data/2.5/group?id={",".join(map(lambda city: str(city["id"]), cities))}&units=metric&appid={weather_key}'
            response = requests.get(url)
            return response.json()['list']

        def is_it_raining(weather):
            weather_code = str(weather['weather'][0]['id'])
            weather_code_first_digit = weather_code[0]
            if weather_code_first_digit == '5':
                return True
            if weather_code_first_digit == '3':
                return True
            if weather_code == '200':
                return True
            if weather_code == '201':
                return True
            if weather_code == '202':
                return True
            if weather_code == '230':
                return True
            if weather_code == '231':
                return True
            if weather_code == '232':
                return True
            return False
        
        found_potential_rainy_cities = False
        times_looked = 0
        where_its_raining = None
        while found_potential_rainy_cities is False:
            if times_looked >= 3:
                print("cannot find any rainy cities... will look again.")
                time.sleep(60)#To not annoy the API
                times_looked = 0
            where_its_raining = list(filter(is_it_raining, get_potential_rainy_cities()))
            times_looked += 1
            if len(where_its_raining) > 0:
                found_potential_rainy_cities = True

        rainy_city = where_its_raining[0]

        post = f'It\'s raining in {rainy_city["name"]}, {countries_list[rainy_city["sys"]["country"]]}. https://www.youtube.com/watch?v=zNd4apsr3WE'
        api.update_status(post)
        mastodon(post)
        time.sleep(3600)



if __name__ == "__main__":
   run()