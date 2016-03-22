# coding=utf-8
import unittest
from selenium import webdriver
from unittestzero import Assert
from pages.home import HomePage
from utils.config import *
from utils.utils import *
from datetime import timedelta, date
from time import sleep
import os
from datetime import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import gmtime, strftime
import re

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)
run_locally = True

# @on_platforms(browsers)
class SmokeTest(unittest.TestCase):
    _internal_non_grouped_domain_text = 1

    def test_register_user_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        register_user_page = home_page.header.open_register_user_page()
        profile_page = register_user_page.register_user()
        sleep(10)

        Assert.equal(register_user_page._name_value, profile_page.get_value_name())
        Assert.equal(register_user_page._surname_value, profile_page.get_value_surname())
        Assert.equal(register_user_page._company_name_value, profile_page.get_value_company_name())
        Assert.equal(register_user_page._NIP_value, profile_page.get_value_NIP())
        Assert.equal(register_user_page._phone_value, profile_page.get_value_phone())

    def test_login_and_logout_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        profile_page = home_page.header.login(USER, PASSWORD)
        home_page.header.logout()



    def tally(self):
        return len(self._resultForDoCleanups.errors) + len(self._resultForDoCleanups.failures)

    def setUp(self):
        self.timeout = 30
        if run_locally:
            self.driver = webdriver.Firefox()
            self.driver.maximize_window()
            self.driver.implicitly_wait(self.timeout)
            self.errors_and_failures = self.tally()
        else:
            self.desired_capabilities['name'] = self.id()
            sauce_url = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub"

            self.driver = webdriver.Remote(
                desired_capabilities=self.desired_capabilities,
                command_executor=sauce_url % (USERNAME, ACCESS_KEY)
            )

            self.driver.implicitly_wait(self.timeout)

    def tearDown(self):
        if run_locally:
                if self.tally() > self.errors_and_failures:
                    if not os.path.exists(SCREEN_DUMP_LOCATION):
                        os.makedirs(SCREEN_DUMP_LOCATION)
                    for ix, handle in enumerate(self.driver.window_handles):
                        self._windowid = ix
                        self.driver.switch_to.window(handle)
                        # self.take_screenshot()
                        # self.dump_html()
                self.driver.quit()

    def not_contains(self, needle, haystack, msg=''):
        try:
            assert not needle in haystack
        except AssertionError:
            raise AssertionError('%s is found in %s. %s' % (needle, haystack, msg))

if __name__ == '__main__':
     unittest.main()
