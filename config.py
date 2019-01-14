#apppication default verbose and log levels
DEFAULT_VERBOSE_LEVEL = 0
DEFAULT_MESSAGE_FORMAT = '%(message)S'


CONFIG_LOCATION = 'Location'
CONFIG_FILE = 'weatherapp.ini'

FAKE_MOZILA_AGENT = 'Mozila/5.0 (X11; Fedora; Linux x86_64;)'

CACHE_DIR = '.wappcache'
CACHE_TIME = 300 


ACCU_PROVIDER_NAME = 'accu'
ACCU_PROVIDER_TITLE = 'AccuWether'
ACCU_URL = ("  https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505")
#ACCU_TAGS = ('<span class="large-temp">', '<span class="cond">')
ACCU_BROWSE_LOCATIONS = 'https://www.accuweather.com/uk/browse-locations'

ACCU_DEFAULT_LOCATION_NAME = 'Kyiv'
ACCU_DEFAULT_LOCATION_URL = 'https://www.accuweather.com/uk/ua/kyiv/324505/weather-forecast/324505'



RP5_PROVIDER_NAME = 'rp5'
RP5_PROVIDER_TITLE = 'Rp5.ua'
RP5_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96")
RP5_CONTAINER = ('<div class="ArchiveInfo" style="width:80%;">')          
RP5_TAGS = ('<span class="t_0" style="">', ' °F</span>, ')
RP5_BROWSE_LOCATIONS = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0"
                        "_%D0%B2_%D1%81%D0%B2%D1%96%D1%82%D1%96")

RP5_DEFAULT_LOCATION_NAME = 'Kyiv'
RP5_DEFAULT_LOCATION_URL = ("http://rp5.ua/%D0%9F%D0%BE%D0%B3%D0%BE%D0%B4%D0%B0_"
                   "%D0%B2_%D0%9A%D0%B8%D1%94%D0%B2%D1%96")
