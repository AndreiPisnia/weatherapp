#!/usr/bin/env python

"""Weather providers.
"""

import re
import time
import hashlib
import configparser
from pathlib import Path
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

import decorators
import config


class WeatherProvider:
    """Base weather provider
    """
    def __init__(self, app):
        self.app = app

        location, url = self.get_configuration()
        self.location = location
        self.url = url


    def get_configuration_file(self):
        """Path to configuration file

        Returns path to configuration file in home directory
        """
        return Path.home() / config.CONFIG_FILE


    def get_configuration(self):
        """Returns configured location, name and url.
        """
#        Raise "ProviderConfigurationError" error if configuration
#        is broken or was not found.
        """
        :return: city name and url
        :rtype: tuple
        """

        name = self.default_location
        url = self.default_url
        configuration = configparser.ConfigParser()
        
        configuration.read(self.get_configuration_file())
        if config.CONFIG_LOCATION in configuration.sections():
            location_config = configuration[config.CONFIG_LOCATION]
            name, url = location_config['name'], location_config['url']
        return name, url


    def save_configuration(self, name, url):
        """Save selected location to configuration file.

        To save time and not configurate application
        each time we going to use it.

        :param name: city name
        :param type: str

        :param url: prefered location URL
        :param type: str
        """
        parser = configparser.ConfigParser()
        parser[config.CONFIG_LOCATION] = {'name': name, 'url': url}
        with open(self.get_configuration_file(), 'w') as configfile:
            parser.write(configfile)


    def get_request_headers(self):
        """Returns custom headers to url requests.
        """
        return {'User-Agent': config.FAKE_MOZILA_AGENT}


    def get_url_hash(self, url):
        """Generates hash for given url
        """
        return hashlib.md5(url.encode('utf-8')).hexdigest()

    def get_cache_directory(self):
        """Path to cache directory
        """
        return Path.home() / config.CACHE_DIR


    def is_valid(self, path):
        """Check if current cache file is valid.
        """

        return (time.time() - path.stat().st_mtime) < config.CACHE_TIME
                 

    def get_cache(self, url):
        """ Return cache data if any.
        """

        cache = b''
        cache_dir = self.get_cache_directory()
        if cache_dir.exists():
            cache_path = cache_dir / self.get_url_hash(url)
            if cache_path.exists() and self.is_valid(cache_path):
                with cache_path.open('rb') as cache_file:
                    cache = cache_file.read()

        return cache


    def save_cache(self, url, page_source):
        """Save page source data to file
        """
        cache_dir = self.get_cache_directory()
        if not cache_dir.exists():
            cache_dir.mkdir(parents=True)
        with (cache_dir / self.get_url_hash(url)).open('wb') as cache_file:
            cache_file.write(page_source)


    def get_page_source(self, url, refresh=False):
        """Use URL and receive requested page decoded by utf-8
        """
        cache = self.get_cache(url)
        if cache and not refresh:
            page_source = cache
#            print(f'Cache for {url}')
        else:
            request = Request(url, headers=self.get_request_headers())
            page_source = urlopen(request).read()
            self.save_cache(url, page_source)
        
        return page_source.decode('utf-8')

    @decorators.one_moment
    def run(self, refresh=False):
        content = self.get_page_source(self.url, refresh=refresh)
        return self.get_weather_info(content, refresh=refresh)


class AccuWeatherProvider(WeatherProvider):
    """Weather provider for Accuweather site.
    """

    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PROVIDER_TITLE

    default_location = config.ACCU_DEFAULT_LOCATION_NAME
    default_url = config.ACCU_DEFAULT_LOCATION_URL

    
    def get_locations(self, locations_url, refresh=False):
        """
        """
        locations_page = self.get_page_source(locations_url, refersh=refresh)
        soup = BeautifulSoup(locations_page, 'html.parser')

        locations = []
        for location in soup.find_all('li', class_='drilldown cl'):
            url = location.find('a').attrs['href']
            location = location.find('em').text
            locations.append((location, url))
        return locations


    def configurate(self, refresh=False):
        """
        """
        locations = self.get_locations(config.ACCU_BROWSE_LOCATIONS, refresh=refresh)
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}. {location[0]}')
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            locations = self.get_locations(location[1], refresh=refresh)

        self.save_configuration(*location)


    def get_weather_info(self, page_content, refresh=False):
        """
        """
        city_page = BeautifulSoup(page_content, 'html.parser')
        current_day_section = city_page.find(
            'li', class_=re.compile('(day|night) current first cl'))

        weather_info = {}
        if current_day_section:
            current_day_url = current_day_section.find('a').attrs['href']
            if current_day_url:
                current_day_page = self.get_page_source(current_day_url,
                                                        refresh=refresh)
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

#_____________________________________________________________________________

class Rp5WeatherProvider(WeatherProvider):
    """Weather provider for Rp5 site.
    """
    name = config.RP5_PROVIDER_NAME
    title = config.RP5_PROVIDER_TITLE

    default_location = config.RP5_DEFAULT_LOCATION_NAME
    default_url = config.RP5_DEFAULT_LOCATION_URL


    def get_countries():
        pass

    def get_cities():
        pass

    def configurate(self, refresh=False):
        """
        """
        locations = self.get_locations(config.RP5_BROWSE_LOCATIONS, refresh=refresh)
        while locations:
            for index, location in enumerate(locations):
                print(f'{index + 1}. {location[0]}')
            selected_index = int(input('Please select location: '))
            location = locations[selected_index - 1]
            locations = self.get_locations(location[1], refresh=refresh)

        self.save_configuration(*location)


    def get_weather_info(self, page_content, refresh=False):
        """
        """
#           This function is not ready yet.
#           Problem with getting information from site Rp5.
#           Still working on this. 


        city_page = BeautifulSoup(page_content, 'html.parser')
        current_day_section = city_page.find(
            'div', class_="ArchiveInfo")

        weather_info = {}
        temp = current_day_section.find('span', class_="t_0")
        weather_info['temp'] = temp.text
     
        weather_info['cond'] = current_day_section.text
#        print(weather_info)

        return weather_info
