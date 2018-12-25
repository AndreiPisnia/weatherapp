#!/usr/bin/env python

'''Weather app progect. Get information from AccuWeather
'''
import sys
import html
import argparse

from providers import AccuWeatherProvider
from providers import Rp5WeatherProvider




#RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_"
#           "%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96")
#RP5_CONTAINER = '<div class="ArchiveInfo" style="width:80%;">'
#RP5_TAGS = ('<span class="t_0" style="">', ' °F</span>, ')
#
#SINOPTIK_URL = "https://ua.sinoptik.ua/%D0%BF%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0-%D0%BA%D0%B8%D1%97%D0%B2"
#SINOPTIK_CONTAINER = '<div class="imgBlock">'
#SINOPTIK_TAGS = ('<p class="today-temp">', 'alt=')


def produce_accu_output(city_name, info):
    """
    """
    print('Accu Weather: \n')
    print(f'{city_name}')
    print('_'*20)
    
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
         
def get_accu_weather_info(refresh=False):
    accu = AccuWeatherProvider()
    produce_accu_output(accu.location, accu.run(refresh=refresh))

def produce_rp5_output(city_name, info):
    """
    """
    print('Rp5 Weather: \n')
    print(f'{city_name}')
    print('_'*20)
    
    for key, value in info.items():
        print(f'{key}: {html.unescape(value)}')
    

def get_rp5_weather_info(refresh=False):
    rp5 = Rp5WeatherProvider()
    produce_rp5_output(rp5.location, rp5.run(refresh=refresh))
    

def main(argv):
    """ Main entry point.
    """

#    print(argv)
#    sys.exit(0)

    KNOWN_COMMANDS = {'accu': get_accu_weather_info,
                      'rp5': get_rp5_weather_info}#,
#                      'config': configurate}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('command', help='Service name', nargs='?')
    parser.add_argument('--refresh', help='Update cache', action='store_true')
    params = parser.parse_args(argv)

#    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS, ACCU_CONTAINER),
#                     "RP5": (RP5_URL, RP5_TAGS, RP5_CONTAINER),
#                     "Sinoptik": (SINOPTIK_URL, SINOPTIK_TAGS, SINOPTIK_CONTAINER)}
    if params.command:
        command = params.command[:]
#        print(command)
        if command in KNOWN_COMMANDS:
             KNOWN_COMMANDS[command](refresh=params.refresh)
        else:
            print('Unknown command provided!')
            sys.exit(1)


if __name__ == '__main__':
    main(sys.argv[1:])


