#!/usr/bin/python3
'''Weather app progect. Get information from AccuWeather
'''
import sys
import html
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

ACCU_URL = "  https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505"
ACCU_CONTAINER = '<li class="night current first cl" data-href="https://www.accuweather.com/uk/ua/kyiv/324505/current-weather/324505">'
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')

RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_"
           "%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96")
RP5_CONTAINER = '<div class="ArchiveInfo" style="width:80%;">'
RP5_TAGS = ('<span class="t_0" style="">', ' °F</span>, ')

SINOPTIK_URL = "https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D1%97%D0%B2"
SINOPTIK_CONTAINER = '<div class="imgBlock">'
SINOPTIK_TAGS = ('<p class="today-temp">', 'alt=')


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

def get_tag_content(page_content, tag, container):
    """Find tag and get information from source page
    """

    tag_index = page_content.find(tag, page_content.find(container))
    tag_size = len(tag)
    value_start = tag_index + tag_size

    content =''
    for c in page_content[value_start:]:
        if c != '<':
            content += c
        else:
            break
    return content

def get_weather_info(page_content):
    """
    """

#    return tuple([get_tag_content(page_content, tag, container) for tag in tags])

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

def produce_output(info):
    """
    """
    print('Accu Weather: \n')

    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
        
#    print(f'\n{provider_name}')
#    print(f'Temperature: {html.unescape(temp)}')
#    print(f'Condition: {condition} \n')
            

def main(argv):
    """ Main entry point.
    """

#    print(argv)
#    sys.exit(0)

    KNOWN_COMMANDS = {'accu': 'AccuWeather', 'rp5': 'RP5', 'sinoptik': 'Sinoptik'}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs=1)
    params = parser.parse_args(argv)

    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS, ACCU_CONTAINER),
                     "RP5": (RP5_URL, RP5_TAGS, RP5_CONTAINER),
                     "Sinoptik": (SINOPTIK_URL, SINOPTIK_TAGS, SINOPTIK_CONTAINER)}
    if params.command:
        command = params.command[0]
        if command in KNOWN_COMMANDS:
            weather_sites = {
                KNOWN_COMMANDS[command]: weather_sites[KNOWN_COMMANDS[command]]
            }
        else:
            print('Unknown command provided!')
            sys.exit(1)


    for name in weather_sites:
        url, tags, container = weather_sites[name]
        content = get_page_source(url)
        produce_output(get_weather_info(content))

if __name__ == '__main__':
    main(sys.argv[1:])


