#!/usr/bin/env python

'''Weather app progect. Get information from AccuWeather
'''
import sys
import html
import argparse
import configparser
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

ACCU_URL = ("  https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505")

ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')

DEFAULT_NAME = 'Kyiv'
DEFAULT_URL = 'https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505'
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'
CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'

#RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_"
#           "%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96")
#RP5_CONTAINER = '<div class="ArchiveInfo" style="width:80%;">'
#RP5_TAGS = ('<span class="t_0" style="">', ' °F</span>, ')
#
#SINOPTIK_URL = "https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D1%97%D0%B2"
#SINOPTIK_CONTAINER = '<div class="imgBlock">'
#SINOPTIK_TAGS = ('<p class="today-temp">', 'alt=')


def get_request_headers():
    """
    """
    return {'User-Agent': 'Mozila/5.0 (X11; Fedora; Linux x86_64;)'}

def get_page_source(url):
    """Use URL and receive requested page decoded by utf-8
    """

    request = Request(url, headers=get_request_headers())
    page_source = urlopen(request).read()
    return page_source.decode('utf-8')

def get_locations(locations_url):
    """
    """
    locations_page = get_page_source(locations_url)
    soup = BeautifulSoup(locations_page, 'html.parser')

    locations = []
    for location in soup.find_all('li', class_='drilldown cl'):
        url = location.find('a').attrs['href']
        location = location.find('em').text
        locations.append((location, url))
    return locations


def get_configuration_file():
    """
    """
    return Path.home() / CONFIG_FILE


def save_configuration(name, url):
    """
    """
    parser = configparser.ConfigParser()
    parser[CONFIG_LOCATION] = {'name': name, 'url': url}
    with open(get_configuration_file(), 'w') as configfile:
        parser.write(configfile)


def get_configuration():
    """
    """
    name = DEFAULT_NAME
    url =  DEFAULT_URL
    
    parser = configparser.ConfigParser()
    parser.read(get_configuration_file())

    if CONFIG_LOCATION in parser.sections():
        config = parser[CONFIG_LOCATION]
        name, url = config['name'], config['url']
    return name, url

    
def configurate():
    """
    """
    locations = get_locations(ACCU_BROWSE_LOCATIONS)
    while locations:
        for index, location in enumerate(locations):
            print(f'{index + 1}. {location[0]}')
        selected_index = int(input('Please select location: '))
        location = locations[selected_index - 1]
        locations = get_locations(location[1])

    save_configuration(*location)

def get_weather_info(page_content):
    """
    """

    city_page = BeautifulSoup(page_content, 'html.parser')
    current_day_section = city_page.find(
        'li', class_='night current first cl')

    weather_info = {}
    if current_day_section:
        current_day_url = current_day_section.find('a').attrs['href']
        if current_day_url:
            current_day_page = get_page_source(current_day_url)
            if current_day_page:
                current_day = \
                        BeautifulSoup(current_day_page, 'html.parser')
                weather_details = \
                        current_day.find('div', attrs={'id': 'detail-now'})
                condition = weather_details.find('span', class_='cond')
                if condition:
                    weather_info['cond'] = condition.text
                temp = weather_details.find('span', class_='large-temp')
                if temp:
                    weather_info['temp'] = temp.text
                feal_temp = weather_details.find('span', class_='small-temp')
                if feal_temp:
                    weather_info['feal_temp'] = feal_temp.text
                wind_info = weather_details.find_all('li', class_='wind')
                if wind_info:
                    weather_info['wind'] = \
                            ' '.join(map(lambda t: t.text.strip(), wind_info))

    return weather_info

def produce_output(city_name, info):
    """
    """
    print('Accu Weather: \n')
    print(f'{city_name}')
    print('_'*20)

    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
        
#    print(f'\n{provider_name}')
#    print(f'Temperature: {html.unescape(temp)}')
#    print(f'Condition: {condition} \n')
            
def get_accu_weather_info():
    city_name, city_url = get_configuration()
    content = get_page_source(city_url)
    produce_output(city_name, get_weather_info(content))

def main(argv):
    """ Main entry point.
    """

#    print(argv)
#    sys.exit(0)

    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'config': configurate}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs='?')
    params = parser.parse_args(argv)

#    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS, ACCU_CONTAINER),
#                     "RP5": (RP5_URL, RP5_TAGS, RP5_CONTAINER),
#                     "Sinoptik": (SINOPTIK_URL, SINOPTIK_TAGS, SINOPTIK_CONTAINER)}
    if params.command:
        command = params.command[:]
#        print(command)
        if command in KNOWN_COMMANDS:
             KNOWN_COMMANDS[command]()
        else:
            print('Unknown command provided!')
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])


