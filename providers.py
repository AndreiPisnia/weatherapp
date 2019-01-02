#!/usr/bin/env python

"""Weather providers.
"""

import re
import urllib

from bs4 import BeautifulSoup

import decorators
import config
from abstract import WeatherProvider


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
