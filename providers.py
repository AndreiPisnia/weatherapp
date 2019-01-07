#!/usr/bin/env python

"""Weather providers.
"""

import re
import urllib

from bs4 import BeautifulSoup

import config
import decorators

from abstract import WeatherProvider


class AccuWeatherProvider(WeatherProvider):
    """Weather provider for Accuweather site.
    """

    name = config.ACCU_PROVIDER_NAME
    title = config.ACCU_PROVIDER_TITLE

    default_location = config.ACCU_DEFAULT_LOCATION_NAME
    default_url = config.ACCU_DEFAULT_LOCATION_URL

    def get_default_location(self):
        return config.ACCU_DEFAULT_LOCATION_NAME

    def get_default_url(self):
        return config.ACCU_DEFAULT_LOCATION_URL


    def get_name(self):
        return self.name
    
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

    def get_name(self):
        return self.name

    default_location = config.RP5_DEFAULT_LOCATION_NAME
    default_url = config.RP5_DEFAULT_LOCATION_URL

    def get_default_location(self):
        return config.RP5_DEFAULT_LOCATION_NAME

    def get_default_url(self):
        return config.RP5_DEFAULT_LOCATION_URL

    def get_countries(self, countries_url):
        countries_page = self.get_page_source(countries_url)
        soup = BeautifulSoup(countries_page, 'html.parser')
        base = urllib.parse.urlunsplit(
            urllib.parse.urlparse(countries_url)[:2] + ('/', '', ''))
        countries = []
        for country in soup.find_all('div', class_='country_map_links'):
            url = urllib.parse.urljoin(base, country.find('a').attrs['href'])
            country = country.find('a').text
            
    def get_cities(self, country_url):
        cities_page = self.get.page.source(country_url)
        soup = BeautifulSoup(country_page, 'html.parser')
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
            print(f'{index + 1}. {country[0]}\n')
        selected_index = int(input('Please select country: '))
        country = countries[selected_index - 1]

        cities = self.get_cities(country[1])
        for index, city in enumerate(cities):
            print(f'{index + 1}. {city[0]}')
        selected_index = int(input('Please select city: '))
        city = cities[selected_index - 1]
#        locations = self.get_locations(location[1], refresh=refresh)

        self.save_configuration(*city)


    def get_weather_info(self, page_content, refresh=False):
        """Get weather information
        """

        city_page = BeautifulSoup(page_content, 'html.parser')
        current_day = city_page.find('div', id="archiveString")
#        current_day = city_page.find('div', class_="ArchiveInfo")

        weather_info = {'cond': '', 'temp': '', 'feal_temp': '', 'wind': ''}

        archive_text = current_day.text
        info_list = archive_text.split(',')
        weather_info['cond'] = info_list[1].strip()
        
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
