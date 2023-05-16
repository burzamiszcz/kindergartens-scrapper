import requests
from bs4 import BeautifulSoup
import googlemaps
import pprint
import re
import config

API_KEY = config.API_KEY

def get_data_from_googlemaps(API_KEY, search_name = 'Przedszkole Wrocław'):
    list = []
    gmaps = googlemaps.Client(key=API_KEY)
    results = gmaps.places(search_name)
    for result in results['results']:
        name = result['name']
        address = result['formatted_address']
        place_id = result['place_id']
        place_details = gmaps.place(place_id = place_id, fields = ['website', 'formatted_phone_number'])
        pprint.pprint(place_details)
        if 'website' in place_details['result']:
            website = place_details['result']['website']
        else:
            continue
        list.append([name, address, website])
    return list

        # with open('wroclaw.csv', 'a', encoding="utf-8") as file:
        #     file.write(f'{name};{address};{website}\n')
        #     print(f'{name}\n {address}\n {website}\n\n')

# get_data_from_googlemaps(API_KEY)
    
def scrap_for_email(url):
    emails = []
    def email_search(direct_url):
        response = requests.get(direct_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            text = soup.get_text()
            email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
            email_addresses = re.findall(email_pattern, text)

            return email_addresses
        else:
            return None
        
    # Pobierz zawartość strony
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Znajdź wszystkie elementy <a>
        anchor_tags = soup.find_all('a')
        # Przeszukaj wszystkie elementy <a> w poszukiwaniu adresu e-mail
        for tag in anchor_tags:
                link = tag.get('href')
                if link and 'przedszkole74' in link:
                    print(link)
                    try:
                        email = email_search(link)
                    except:
                        pass
                    if email:
                        emails += email
        print(emails)
    else:
        print('Nie można pobrać strony.')

scrap_for_email('https://przedszkole74.edu.wroclaw.pl/')