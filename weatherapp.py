#!/usr/bin/python3
'''Weather app progect
'''
import sys
import html
import argparse
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

def get_weather_info(page_content, tags, container):
    """
    """

    return tuple([get_tag_content(page_content, tag, container) for tag in tags])

def produce_output(provider_name, temp, condition):
    """
    """
    print(f'\n{provider_name}')
    print(f'Temperature: {html.unescape(temp)}')
    print(f'Condition: {condition} \n')
            

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
        temp, condition = get_weather_info(content, tags, container)
        produce_output(name, temp, condition)

if __name__ == '__main__':
    main(sys.argv[1:])


