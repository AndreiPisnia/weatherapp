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
accu_page = accu_page.decode('utf-8')

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

# getting temperature from == RP5 ==
RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_"
           "%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96")

rp5_request = Request(RP5_URL, headers=headers)
rp5_page = urlopen(rp5_request).read()
rp5_content = rp5_page.decode('utf-8')

WINFO_CONTAINER_TAG = '<div id="ArchTemp">'
RP5_TEMP_TAG = '<span class="t_0" style="display: block;">'
rp5_temp_tag_index = rp5_content.find(RP5_TEMP_TAG,
                                rp5_content.find(WINFO_CONTAINER_TAG))
rp5_temp_tag_size = len(RP5_TEMP_TAG)
rp5_temp_value_start = rp5_temp_tag_index + rp5_temp_tag_size
rp5_temp = ''
for char in rp5_content[rp5_temp_value_start:]:
    if char != '<':
        rp5_temp += char
    else:
        break

print('RP5.UA: \n')
print(f'Temperature: {html.unescape(rp5_temp)} \n')

# getting conditions from == RP5 ==
COND_INFO_CONTAINER_TAG = '<div id="forecastShort-content">'
RP5_COND_TAG = '<span class="second-part">'
rp5_cond_value_end_index = rp5_content.find(RP5_COND_TAG,
                                rp5_content.find(COND_INFO_CONTAINER_TAG))

rp5_cond_value_start = rp5_cond_value_end_index
while rp5_content[rp5_cond_value_start] != '>':
    rp5_cond_value_start -= 1
rp5_cond = rp5_content[rp5_cond_value_start:rp5_cond_value_end_index]    

print(f'Condition: {rp5_cond} \n')
