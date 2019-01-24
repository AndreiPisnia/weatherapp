#!/usr/bin/env python

"""Weather providers.
"""

import re
import sys
import urllib
import logging


from bs4 import BeautifulSoup

from weatherapp.core import config
from weatherapp.core import decorators

from weatherapp.core.abstract.provider import WeatherProvider

class Rp5WeatherProvider(WeatherProvider):
    """Weather provider for Rp5 site.
    """

    stdout = sys.stdout
    logger = logging.getLogger('')
        
    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    def get_name(self):
        return self.name

    default_location = config.RP5_DEFAULT_LOCATION_NAME
    default_url = config.RP5_DEFAULT_LOCATION_URL

    def get_default_location(self):
        return config.RP5_DEFAULT_LOCATION_NAME

    def get_default_url(self):
        return config.RP5_DEFAULT_LOCATION_URL

    def get_countries(self, countries_url, refresh=False):
        countries_page = self.get_page_source(countries_url)
        soup = BeautifulSoup(countries_page, 'html.parser')
        base = urllib.parse.urlunsplit(
            urllib.parse.urlparse(countries_url)[:2] + ('/', '', ''))
        countries = []
        for country in soup.find_all('div', class_='country_map_links'):
            url = urllib.parse.urljoin(base, country.find('a').attrs['href'])
            country = country.find('a').text
            countries.append((country, url))
        return countries
            
    def get_cities(self, country_url):
        cities = []
        cities_page = self.get_page_source(country_url)
        soup = BeautifulSoup(cities_page, 'html.parser')
        base = urllib.parse.urlunsplit(
            urllib.parse.urlparse(country_url)[:2] + ('/', '', ''))
        country_map = soup.find('div', class_='countryMap')
        if country_map:
            cities_list = country_map.find_all('h3')
            for city in cities_list:
                url = urllib.parse.urljoin(base, city.find('a').attrs['href'])
                city = city.find('a').text
                cities.append((city, url))
        return cities

    def configurate(self, refresh=False):
        """Configure provider.
        """
        countries = self.get_countries(config.RP5_BROWSE_LOCATIONS, refresh=refresh)
        for index, country in enumerate(countries):
            self.stdout.write(f'{index + 1}. {country[0]}\n')
#            print(f'{index + 1}. {country[0]}\n')
        try:
            selected_index = int(input('Please select country: '))
        except ValueError:
            self.stdout.write("Wrong choice."
                  "Please restart configuration and input the number. \n")
            exit()

        try:
            country = countries[selected_index - 1]
        except IndexError:
            self.stdout.write(f"Wrong choice: {selected_index}. "
                  "Please make wright selection. \n")
            exit()

        cities = self.get_cities(country[1])
        for index, city in enumerate(cities):
            self.stdout.write(f'{index + 1}. {city[0]} \n')        
#            print(f'{index + 1}. {city[0]}')
        try:
            selected_index = int(input('Please select city: '))
        except ValueError:
            self.stdout.write("Wrong choice."
                  "Please restart configuration and input the number. \n")
            exit()
        try:
            city = cities[selected_index - 1]
        except IndexError:
            self.stdout.write(f"Wrong choice: {selected_index}. "
                  "Please make wright selection. \n")
            exit()
            
#        locations = self.get_locations(location[1], refresh=refresh)

        self.save_configuration(*city)


    def get_weather_info(self, page_content, refresh=False):
        """Get weather information
        """

        city_page = BeautifulSoup(page_content, 'html.parser')
        current_day = city_page.find('div', id="archiveString")
#        current_day = city_page.find('div', class_="ArchiveInfo")
        weather_info = {'cond': '', 'temp': '', 'feal_temp': '', 'wind': ''}
#        print (weather_info)
        archive_text = current_day.text
        info_list = archive_text.split(',')
#        self.logger.debug('Got the following args %s', argv)
#        print(info_list)
        try:
            weather_info['cond'] = info_list[1].strip()
        except IndexError:
            print('Conditions are not available right now.')
#            msg = "Error during command: %s run"
#            self.logger.exception(msg)#, command_name)                
        
        temp = current_day.find('span', class_="t_0")
        weather_info['temp'] = temp.text
        
#        if current_day:
#            import pdb; pdb.set_trace()
#            archive_info = current_day.find('div', class_="ArchiveInfo")
#            if archive_info:
#                archive_text = archive_info.text
#                info_list = archive_text.split(',')
#                weather_info['cond'] = info_list[1].strip()
#                temp = archive_info.find('span', class_='t=0')
#                if temp:
#                    weather_info['temp'] = temp.text
#                wind = info_list[3].strip()[:info_list[3].find(')')]
#                wind += info_list[4]
#                if wind:
#                    weather_info['wind'] = wind

        return weather_info
