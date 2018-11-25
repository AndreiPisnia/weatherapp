#!/usr/bin/python3
'''Weather app progect
'''
import html
from urllib.request import urlopen, Request

ACCU_URL = " https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505"
ACCU_CONTAINER = ('<li class="night current first cl" data-href="https://www.accuweather.com/uk/ua/kyiv/324505/current-weather/324505">')
ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')

#'<span class="t_0" style="display: block;">'

# getting conditions from == RP5 ==
#COND_INFO_CONTAINER_TAG = '<div id="forecastShort-content">'
#RP5_COND_TAG = '<span class="second-part">'
#rp5_cond_value_end_index = rp5_content.find(RP5_COND_TAG,
#                                rp5_content.find(COND_INFO_CONTAINER_TAG))
#
#rp5_cond_value_start = rp5_cond_value_end_index
#while rp5_content[rp5_cond_value_start] != '>':
#    rp5_cond_value_start -= 1
#rp5_cond = rp5_content[rp5_cond_value_start:rp5_cond_value_end_index]    
#
#print(f'Condition: {rp5_cond} \n')

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

def get_tag_content(page_content, container, tag):
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

def get_weather_info(page_content, container, tags):
    """
    """

    return tuple([get_tag_content(page_content, container, tag) for tag in tags])

def produce_output(provider_name, temp, condition):
    """
    """
    print(f'\n{provider_name}')
    print(f'Temperature: {html.unescape(temp)} \n')
    print(f'Condition: {condition} \n')
            

def main():
    """ Main entry point.
    """

    weather_sites = {"AccuWeather": (ACCU_URL, ACCU_TAGS, ACCU_CONTAINER)} #"RP5": (RP5_URL, RP5_TAGS)}
    for name in weather_sites:
        url, container, tags = weather_sites[name]
        content = get_page_source(url)
        temp, condition = get_weather_info(content, tags, container)
        produce_output(name, temp, condition)

if __name__ == '__main__':
    main()


