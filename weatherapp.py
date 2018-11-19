#!/usr/bin/python3
'''Weather app progect
'''
import html
from urllib.request import urlopen, Request

ACCU_URL = " https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505"
#Change language to english if can't get conditions in ukrainian.
#ACCU_URL = " https://www.accuweather.com/en/ua/kyiv/324505/weather-forecast/324505?lang=en-us"

# getting page from server
headers = {'User-Agent': 'Mozila/5.0 (X11; Fedora; Linux x86_64;)'}
accu_request = Request(ACCU_URL, headers=headers)
accu_page = urlopen(accu_request).read()
accu_page = str(accu_page, 'utf-8')

# getting temperature
ACCU_TEMP_TAG = '<span class="large-temp">'
accu_temp_tag_size = len(ACCU_TEMP_TAG)
accu_temp_tag_index = accu_page.find(ACCU_TEMP_TAG)
accu_temp_value_start = accu_temp_tag_index + accu_temp_tag_size
accu_temp = ''
for char in accu_page[accu_temp_value_start:]:
    if char != '<':
        accu_temp += char
    else:
        break

print('AccuWeather: \n')
print(f'Temperature: {html.unescape(accu_temp)} \n')

# getting conditions
ACCU_COND_TAG = '<span class="cond">'
accu_cond_tag_size = len(ACCU_COND_TAG)
accu_cond_tag_index = accu_page.find(ACCU_COND_TAG)

accu_cond_value_start = accu_cond_tag_index + accu_cond_tag_size
accu_cond = ''
char_html = ''
for char in accu_page[accu_cond_value_start:]:
    if char != '<':
        char_html = html.unescape(char)
        accu_cond += char_html
    else:
        break
      
print(f'Condition: {accu_cond} \n')
