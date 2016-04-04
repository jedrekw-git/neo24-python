# coding=utf-8
import unittest
from selenium import webdriver
from htmltestrunner import HTMLTestRunner
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
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import re
from change_password import *

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)
run_locally = True

# @on_platforms(browsers)


class SmokeTest(unittest.TestCase):
    _internal_non_grouped_domain_text = 1

    # def test_register_user_should_succeed(self):
    #
    #     home_page = HomePage(self.driver).open_home_page()
    #     register_user_page = home_page.header.open_register_user_page()
    #     profile_page = register_user_page.register_user()
    #     sleep(10)
    #
    #     Assert.equal(register_user_page._name_value, profile_page.get_value_name())
    #     Assert.equal(register_user_page._surname_value, profile_page.get_value_surname())
    #     Assert.equal(register_user_page._company_name_value, profile_page.get_value_company_name())
    #     Assert.equal(register_user_page._NIP_value, profile_page.get_value_NIP())
    #     Assert.equal(register_user_page._phone_value, profile_page.get_value_phone())
    #
    # def test_change_password_should_succeed(self):
    #     home_page = HomePage(self.driver).open_home_page()
    #     _saved_password = get_password("change_pass2.txt")
    #     login_page = home_page.header.login(CHANGE_PASSWORD_USER, _saved_password)
    #     profile_page = home_page.header.open_my_profile_page()
    #     profile_page.change_password()

    def test_add_to_basket_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        TV_page = home_page.header.open_TV_page()
        TV_page.get_first_product_name_and_price()
        sleep(3)
        TV_page.add_first_product_to_basket()
        WebDriverWait(self.driver, 30).until(EC.invisibility_of_element_located(TV_page._processing_info))
        TV_page.product_added_to_basket_text()

        Assert.equal(TV_page.product_added_to_basket_confirmation, u"dodany do koszyka")
        Assert.equal(TV_page.product_added_to_basket_product_name, TV_page.first_product_name)
        Assert.equal(TV_page.product_added_to_basket_price, TV_page.first_product_price)
        Assert.equal(TV_page.product_added_to_basket_summary_price, TV_page.first_product_price)

        TV_page.go_to_basket()
        TV_page.product_in_basket_text()

        Assert.equal(TV_page.product_in_basket_product_name, TV_page.first_product_name)
        Assert.equal(TV_page.product_in_basket_price, TV_page.first_product_price)
        Assert.equal(TV_page.product_in_basket_summary_price, TV_page.first_product_price)

        TV_page.remove_first_product_from_basket()
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(TV_page._basket_empty_text_field, u"Koszyk jest pusty"))
        TV_page.go_back_to_shopping()
        TV_page.go_to_basket()

        Assert.not_contains(TV_page.first_product_name, TV_page.get_page_source())
        Assert.not_contains(TV_page.first_product_price, TV_page.get_page_source())

    def test_zz_generate_plot_and_send_email(self):
        self._save_plot()
        self._send_email()

    def tally(self):
        return len(self._resultForDoCleanups.errors) + len(self._resultForDoCleanups.failures)

    def setUp(self):
        self.timeout = 30
        if run_locally:
            binary = FirefoxBinary('/__stare/firefox/firefox')
            self.driver = webdriver.Firefox(firefox_binary=binary)
            self.driver.set_window_size(1024,768)
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
                        self.take_screenshot()
                        self.dump_html()
                self.driver.quit()

    def _get_filename(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        self._saved_filename = "{classname}.{method}-window{windowid}-{timestamp}".format(
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )
        return "{folder}/{classname}.{method}-window{windowid}-{timestamp}".format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            method=self._testMethodName,
            windowid=self._windowid,
            timestamp=timestamp
        )

    def _get_filename_for_plot(self):
        timestamp = datetime.now().isoformat().replace(':', '.')[:19]
        self._saved_filename_plot = "{classname}.plot-{timestamp}".format(
            classname=self.__class__.__name__,
            timestamp=timestamp
        )
        return "{folder}/{classname}.plot-{timestamp}".format(
            folder=SCREEN_DUMP_LOCATION,
            classname=self.__class__.__name__,
            timestamp=timestamp
            )

    def _save_plot(self):
        import matplotlib.pyplot as plt
        filename = self._get_filename_for_plot() + ".png"
        err = len(self._resultForDoCleanups.errors) + len(self._resultForDoCleanups.failures)

        # The slices will be ordered and plotted counter-clockwise.
        labels = 'Errors', 'Passes'
        sizes = [err, 113-err]
        colors = ['red', 'gold']
        explode = (0, 0.1)

        plt.pie(sizes, explode=explode, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=90)
        plt.axis('equal')
        print "\n WYKRES:\n", filename
        plt.savefig(filename)
        text_file = open("Neo24RaportScreeny.txt", "a")
        text_file.write("<br><br>Wykres statystyczny: <a href=""http://ci.testuj.pl/job/Neo24/ws/screendumps/"+self._saved_filename_plot+".png>Wykres</a>")
        text_file.close()

    def take_screenshot(self):
        filename = self._get_filename() + ".png"
        print "\n{method} Screenshot and HTML:\n".format(
            method=self._testMethodName)
        print 'screenshot:', filename
        self.driver.get_screenshot_as_file(filename)
        text_file = open("Neo24RaportScreeny.txt", "a")
        text_file.write("<br><br>{method} Screenshot and HTML:<br>".format(
            method=self._testMethodName)+"<br>Screenshot: <a href=""http://ci.testuj.pl/job/Neo24/ws/screendumps/"+self._saved_filename+".png>"+self._saved_filename+"</a>")
        text_file.close()

    def dump_html(self):
        filename = self._get_filename() + '.html'
        print 'page HTML:', filename
        with open(filename, 'w') as f:
            f.write(self.driver.page_source.encode('utf-8'))
        text_file = open("Neo24RaportScreeny.txt", "a")
        text_file.write("<br>Html: <a href=""http://ci.testuj.pl/job/Neo24/ws/screendumps/"+self._saved_filename+".html>"+self._saved_filename+"</a>")
        text_file.close()

    def _send_email(self):
        from mailer import Mailer
        from mailer import Message

        message = Message(From="jedrzej.wojcieszczyk@testuj.pl",
                          To=["jedrzej.wojcieszczyk@testuj.pl"])
        message.Subject = "Raport Jenkins Neo24 Testy Automatyczne"
        message.Html = """<head><meta http-equiv="Content-Type" content="text/html;charset=UTF-8"></head><p>Cześć!<br>
           Oto wygenerowany automatycznie raport z testów Neo24.pl<br><br>
           Tabela raportowa z logami wykonanych testów, a pod nią linki do screenshotów i kodu html testów które nie przeszły oraz wykres statystyczny: <a href="http://ci.testuj.pl/job/Neo24/ws/Neo24ReportLogi.htm">Tabela z logami, screenshoty i wykres</a></p>"""

        sender = Mailer('smtp.gmail.com', use_tls=True, usr='jedrzej.wojcieszczyk@testuj.pl', pwd='paluch88')
        sender.send(message)

    def not_contains(self, needle, haystack, msg=''):
        try:
            assert not needle in haystack
        except AssertionError:
            raise AssertionError('%s is found in %s. %s' % (needle, haystack, msg))

open("Neo24RaportScreeny.txt", 'w').close()
suite = unittest.TestLoader().loadTestsFromTestCase(SmokeTest)
outfile = open("Neo24ReportLogi.htm", "wb")
runner = HTMLTestRunner(stream=outfile, title='Test Report', description='Neo24', verbosity=2)
runner.run(suite)

     # htmltestrunner.main()
# if __name__ == '__main__':
#      unittest.main()

     # import xmlrunner
     # unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))