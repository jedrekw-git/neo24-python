import os
from sauceclient import SauceClient

USERNAME = os.environ.get('SAUCE_USERNAME', "testuj")
ACCESS_KEY = os.environ.get('SAUCE_ACCESS_KEY', "0029898f-54be-48b2-9166-9306282bef0c")
sauce = SauceClient(USERNAME, ACCESS_KEY)

USER = "testujpl@o2.pl"
PASSWORD = "paluch88"

# browsers = [{"platform": "Windows 8.1",
#              "browserName": "internet explorer",
#              "version": "8"},
#             {"platform": "Windows 8.1",
#              "browserName": "firefox",
#              "version": "35"}]