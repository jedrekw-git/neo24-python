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

SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)
run_locally = True

# @on_platforms(browsers)


class SmokeTest(unittest.TestCase):
    _internal_non_grouped_domain_text = 1

    def test_login_wrong_credentials_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(get_random_string(7), get_random_uuid(6))

        Assert.contains(u"Nieprawidłowy login lub hasło", account_page.get_page_source())

    def test_remind_password_wrong_login_should_succeed(self):

        login = get_random_string(7)

        home_page = HomePage(self.driver).open_home_page()
        remind_page = home_page.header.remind_password(login)

        Assert.contains(u"Podany login nie istnieje", remind_page.get_page_source())

    def test_change_contact_data_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_contact_data_page = settings_page.open_change_contact_data_page()
        settings_page.fill_change_contact_data_form()
        settings_page.save_change_contact_data()

        Assert.contains(u"Poniższe dane wskazują osobę, z którą będziemy mogli skontaktować się w sprawach dotyczących twojego konta.", settings_page.get_page_source())
        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())
        Assert.contains(settings_page._change_contact_data_name_value, settings_page.change_contact_data_name_field_text())
        Assert.contains(settings_page._change_contact_data_address_value, settings_page.change_contact_data_address_field_text())
        Assert.contains(settings_page.change_contact_data_postalcode_field_text(), settings_page._change_contact_data_postalcode_value)
        Assert.contains(settings_page._change_contact_data_city_value, settings_page.change_contact_data_city_field_text())

    def test_change_notification_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_notification_settings_page = settings_page.open_change_notification_settings_page()
        settings_page.change_notification_settings()
        settings_page.save_change_notification_settings()

#Brak informacji potwierdzającej

    def test_change_newsletter_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_newsletter_settings_page = settings_page.open_change_newsletter_settings_page()
        settings_page.change_newsletter_settings()
        settings_page.save_change_notification_settings()

#Brak informacji potwierdzającej

    def test_add_email_address_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        add_email_page = settings_page.open_add_email_address_page()
        settings_page.add_email_address()

        Assert.contains(u"Potwierdź adres email", settings_page.get_page_source())

        settings_page.back_to_email_addresses_list()

        Assert.equal(settings_page._add_email_address_value, settings_page.added_email_address_text())
        Assert.equal("Niepotwierdzony", settings_page.added_email_status_text())

        settings_page.remove_added_email_address()

        self.not_contains(settings_page._add_email_address_value, settings_page.get_page_source())
        self.not_contains("Niepotwierdzony", settings_page.get_page_source())

    def test_change_SMS_notification_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        settings_page = account_page.header.open_settings_page()
        change_sms_notification_page = settings_page.open_sms_notification_settings_page()
        settings_page.change_sms_notification_settings()

#Brak informacji potwierdzającej

    def test_add_other_users_to_account_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        add_other_users_page = settings_page.open_add_other_users_page()
        settings_page.add_other_user()

        Assert.contains(u"Operacja wykonana poprawnie.", settings_page.get_page_source())
        sleep(7)
        account_page.header.open_settings_page()
        settings_page.open_add_other_users_page()
        # WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(settings_page._add_other_user_added_login_field, settings_page._add_other_user_login_value))

        Assert.equal(settings_page._add_other_user_login_value, settings_page.added_user_login_text())
        Assert.equal(settings_page._add_other_user_description_value, settings_page.added_user_description_text())

        settings_page.add_other_user_change_priviledges()
#nie ma potwierdzenia

        settings_page.remove_added_user()

        self.not_contains(settings_page._add_other_user_login_value, settings_page.get_page_source())
        self.not_contains(settings_page._add_other_user_description_value, settings_page.get_page_source())

    # def test_change_company_address_should_succeed(self):
    #     home_page = HomePage(self.driver).open_home_page()
    #     account_page = home_page.header.login(USER, PASSWORD)
    #     settings_page = account_page.header.open_settings_page()
    #     change_company_address_page = settings_page.open_change_company_data_page()
    #     settings_page.edit_company_address()
    #
    #     Assert.contains("Operacja wykonana poprawnie", settings_page.edit_company_data_operation_successful_text())
    #     Assert.contains(settings_page.edit_company_data_zip_text(), settings_page._change_company_data_zip_value)
    #     Assert.equal(settings_page._change_company_data_street_value, settings_page.edit_company_data_street_text())
    #     Assert.equal(settings_page._change_company_data_city_value, settings_page.edit_company_data_city_text())

#NIE DA SIĘ?

    def test_change_company_data_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_company_data_page = settings_page.open_change_company_data_page()
        settings_page.edit_company_data()

        Assert.contains(settings_page.edit_company_data_zip_text(), settings_page._change_company_data_zip_value)
        Assert.equal(settings_page._change_company_data_street_value, settings_page.edit_company_data_street_text())
        Assert.equal(settings_page._change_company_data_city_value, settings_page.edit_company_data_city_text())
        Assert.equal(settings_page._change_company_data_company_name_value, settings_page.edit_company_data_company_name_text())
        Assert.equal(settings_page._change_company_data_nip_value, settings_page.edit_company_data_nip_text())

    def test_add_new_bank_account_should_succeed(self):

        number = "26105014451000002276470461"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        bank_accounts_page = settings_page.open_add_bank_account_page()
        settings_page.add_bank_account(number)

        Assert.contains(u"Operacja wykonana poprawnie.", settings_page.get_page_source())
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(settings_page._added_bank_account_number, number))
        Assert.contains("Lista kont bankowych", settings_page.get_page_source())
        Assert.contains(u"Na tej liście znajdują się konta bankowe, na które możesz zlecać wypłaty.", settings_page.get_page_source())
        Assert.contains("Oto lista twoich kont bankowych.", settings_page.get_page_source())
        Assert.equal(settings_page._add_bank_account_account_name_value, settings_page.added_bank_account_name_text())

        settings_page.remove_added_bank_account()
        Assert.contains(u"Operacja wykonana poprawnie.", settings_page.get_page_source())
        sleep(7)

        Assert.contains("Lista kont bankowych", settings_page.get_page_source())
        Assert.contains(u"Na tej liście znajdują się konta bankowe, na które możesz zlecać wypłaty.", settings_page.get_page_source())
        Assert.contains("Oto lista twoich kont bankowych.", settings_page.get_page_source())
        Assert.contains(u"Brak zdefiniowanych kont bankowych", settings_page.get_page_source())
        self.not_contains(number, settings_page.get_page_source())
        self.not_contains(settings_page._add_bank_account_account_name_value, settings_page.get_page_source())

    def test_change_DNS_servers_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        dns_servers_page = settings_page.open_change_DNS_servers_page()
        settings_page.change_DNS_servers()

        Assert.equal("ns1.aftermarket.pl", settings_page.change_DNS_servers_DNS1_text())
        Assert.equal("ns2.aftermarket.pl", settings_page.change_DNS_servers_DNS2_text())
        Assert.equal(settings_page._change_DNS_servers_DNS3_value, settings_page.change_DNS_servers_DNS3_text())
        Assert.equal(settings_page._change_DNS_servers_DNS4_value, settings_page.change_DNS_servers_DNS4_text())
        Assert.equal("Operacja wykonana poprawnie", settings_page.change_DNS_servers_operation_successful_text())

# SERWERY 3 i 4 zamieniają się miejscami z 1 i 2 lub losowo, zgłoszone

    def test_new_DNS_profile_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        dns_profile_page = settings_page.open_new_DNS_profile_page()
        settings_page.new_DNS_profile()

        Assert.contains(u"Operacja wykonana poprawnie.", settings_page.get_page_source())
        sleep(7)
        settings_page.new_DNS_entry()

        Assert.equal("Operacja wykonana poprawnie", settings_page.new_DNS_profile_successful_operation_text())
        Assert.equal(settings_page._new_DNS_profile_name_value, settings_page.new_DNS_profile_successtul_opertation_profile_text())
        Assert.equal(settings_page._new_DNS_profile_host_value, settings_page.new_DNS_profile_successtul_opertation_host_text())
        Assert.equal(settings_page._new_DNS_profile_address_value, settings_page.new_DNS_profile_successtul_opertation_address_text())

        settings_page = account_page.header.open_settings_page()
        dns_profile_page = settings_page.open_new_DNS_profile_page()

        Assert.contains("Lista profili DNS", settings_page.get_page_source())
        Assert.equal(settings_page._new_DNS_profile_name_value, settings_page.new_DNS_profile_name_text())

        settings_page.delete_added_profile()

        self.not_contains(settings_page._new_DNS_profile_name_value, settings_page.get_page_source())

    def test_notification_about_ending_auctions_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        notification_page = settings_page.open_notifications_about_ending_auctions_page()
        settings_page.change_notifications_about_ending_auctions()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_domain_watching_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        domain_watching_settings__page = settings_page.open_domain_watching_settings_page()
        settings_page.change_domain_watching_settings()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_sellers_watching_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        sellers_watching_settings__page = settings_page.open_sellers_watching_settings_page()
        settings_page.change_sellers_watching_settings()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_change_seller_profile_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        change_seller_profile__page = settings_page.open_change_seller_profile_page()
        settings_page.change_seller_profile()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())
        Assert.equal(settings_page._change_seller_profile_description_value, settings_page.change_seller_profile_description_text())

    def test_sending_notification_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        settings_page = account_page.header.open_settings_page()
        sending_notification_settings_page = settings_page.open_sending_notification_settings_page()
        settings_page.change_sending_notification_settings()

        Assert.contains("Operacja wykonana poprawnie", settings_page.get_page_source())

    def test_task_list_filtering_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        task_list = account_page.header.open_task_list()
        task_list.get_text_selected_option()
        task_list.select_operation_type()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(task_list._first_result, task_list.option_text))
        Assert.contains(u"Rodzaj operacji: <b>%s" % task_list.option_text, task_list.get_page_source())

    def test_register_domain_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        register_domain_page = account_page.header.open_register_domain_page()
        register_domain_page.enter_domain_to_register()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(register_domain_page._domain_status_field, u"Dostępna do rejestracji"))

        register_domain_page.register_domain()

        WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element(register_domain_page._registration_effect_domain_field, register_domain_page._domain_name_value))
        WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element(register_domain_page._registration_effect_text_field, u"Domena zarezerwowana i oczekuje na opłacenie"))
        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, register_domain_page._domain_name_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Rejestracja domeny"))

        to_pay_list.remove_first_payment()

        self.not_contains(register_domain_page._domain_name_value, to_pay_list.get_page_source())
        self.not_contains(u"Rejestracja domeny", to_pay_list.get_page_source())

    def test_renew_domain_automatically_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.renew_domain_automatically()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_renew_domain_manually_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.renew_domain_manually()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._second_stage_text_field, u"Domena zostanie odnowiona"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.second_stage_domain_text())

        registered_domains_page.second_stage_checkboxes_and_submit()

        sleep(10)
        if u"Operacja zawieszona, oczekuje na aktywowanie" in registered_domains_page.result_text():
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena już była odnowiona w ostatnim okresie: "))
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, registered_domains_page._first_domain_text_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Odnowienie domeny"))

        to_pay_list.remove_first_payment()

        self.not_contains(registered_domains_page._first_domain_text_value, to_pay_list.get_page_source())
        self.not_contains(u"Odnowienie domeny", to_pay_list.get_page_source())

    def test_change_profile_data_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.change_profile_data()

        sleep(10)
        if u"Operacja wykonana poprawnie" in registered_domains_page.result_text():
            Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena jest zablokowana:"))
            Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

    def test_privacy_settings_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.privacy_settings_first_stage()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._second_stage_text_field, u"Dane abonenta będą widoczne"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.second_stage_domain_text())

        registered_domains_page.second_stage_checkboxes_and_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_get_authinfo_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.get_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_move_domain_from_account_should_succeed(self):

        login = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.move_domain_from_account(login)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer został zainicjowany"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_from_account_list()
        transfer_domain_page.cancel_first_domain_transfer()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Transfer zostanie anulowany"))
        Assert.equal(registered_domains_page._second_domain_text_value, transfer_domain_page.stage2_domain_text())

        transfer_domain_page.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer został anulowany"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_from_account_list()

        self.not_contains(registered_domains_page._second_domain_text_value, transfer_domain_page.get_page_source())


#PRZY TRZECIEJ DOMENIE NA KONCIE DELTA BLĄD, A POZOSTAŁYCH SIE NIE DA PRZENOSIC CALKIEM, zgłośić?????

    def test_change_DNS_servers_for_selected_domain_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.change_dns_servers_for_selected_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_redirection_direct_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_redirection_direct()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_redirection_hidden_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_redirection_hidden()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_redirection_ip_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_redirection_ip()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_dns_profile_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_dns_profile()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_new_dns_entry_for_selected_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.new_dns_entry_for_selected_domain()

        self.not_contains(registered_domains_page._add_dns_entry_host_name_value, registered_domains_page.get_page_source())
        self.not_contains(registered_domains_page._add_dns_entry_address_value, registered_domains_page.get_page_source())

        registered_domains_page.new_dns_entry_for_selected_domain_details()

        Assert.contains("Operacja wykonana poprawnie", registered_domains_page.get_page_source())

        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.select_first_domain()
        registered_domains_page.new_dns_entry_for_selected_domain()

        Assert.contains(registered_domains_page._add_dns_entry_host_name_value, registered_domains_page.get_page_source())
        Assert.contains(registered_domains_page._add_dns_entry_priority_value, registered_domains_page.get_page_source())
        Assert.contains(registered_domains_page._add_dns_entry_address_value, registered_domains_page.get_page_source())

        registered_domains_page.delete_new_dns_entry_for_selected_domain()

        self.not_contains(registered_domains_page._add_dns_entry_host_name_value, registered_domains_page.get_page_source())
        self.not_contains(registered_domains_page._add_dns_entry_address_value, registered_domains_page.get_page_source())

    def test_new_dns_server_in_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.dns_servers_in_domain()

        self.not_contains(registered_domains_page._new_dns_server_in_domain_name_value+"."+registered_domains_page._first_domain_text_value, registered_domains_page.get_page_source())
        self.not_contains(registered_domains_page._new_dns_server_in_domain_ip_value, registered_domains_page.get_page_source())

        registered_domains_page.new_dns_server_in_domain_details()
        Assert.contains(u"Operacja wykonana poprawnie.", registered_domains_page.get_page_source())
        sleep(7)

        Assert.contains(registered_domains_page._new_dns_server_in_domain_name_value+"."+registered_domains_page._first_domain_text_value, registered_domains_page.get_page_source())
        Assert.contains(registered_domains_page._new_dns_server_in_domain_ip_value, registered_domains_page.get_page_source())

        registered_domains_page.delete_new_dns_server_in_domain()

        self.not_contains(registered_domains_page._new_dns_server_in_domain_name_value+"."+registered_domains_page._first_domain_text_value, registered_domains_page.get_page_source())
        self.not_contains(registered_domains_page._new_dns_server_in_domain_ip_value, registered_domains_page.get_page_source())

    def test_change_parking_service_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_parking_service()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_change_keyword_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        registered_domains_page.select_first_domain()
        registered_domains_page.change_keyword()

        sleep(10)
        if "Domena odnowiona poprawnie" in registered_domains_page.result_text():
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page._result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Domena nie jest zaparkowana"))
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

    def test_sell_on_auction_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.sell_on_auction()

        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.sell_on_auction_stage2_domain_text())
        Assert.equal(u"Technologia » Komputery", registered_domains_page.sell_on_auction_stage2_category_text())

        registered_domains_page.sell_on_auction_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Aukcja została wystawiona"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.delete_first_auction()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._second_stage_text_field, u"Aukcja zostanie anulowana"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.second_stage_domain_text())
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(selling_auction_page._submit_button))

        selling_auction_page.delete_auction_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Aukcja została anulowana"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

        selling_auction_page.back_from_results_page()

        self.not_contains(registered_domains_page._second_domain_text_value, selling_auction_page.get_page_source())

    def test_sell_on_auction_edit_details_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.sell_on_auction()

        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.sell_on_auction_stage2_domain_text())
        Assert.equal(u"Technologia » Komputery", registered_domains_page.sell_on_auction_stage2_category_text())

        registered_domains_page.sell_on_auction_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Aukcja została wystawiona"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.first_auction_enter_edit_prices()

        Assert.contains(registered_domains_page._second_domain_text_value, selling_auction_page.get_page_source())
        Assert.contains(str(registered_domains_page._sell_on_auction_price_start_value), selling_auction_page.get_page_source())

        selling_auction_page.edit_auction_prices()
        sleep(2)
        Assert.contains(u"Operacja wykonana poprawnie.", selling_auction_page.get_page_source())
        sleep(7)
        selling_auction_page.back_from_results_page()

        Assert.contains(registered_domains_page._second_domain_text_value, selling_auction_page.get_page_source())
        Assert.contains(str(selling_auction_page._edit_auction_details_price_start_value), selling_auction_page.get_page_source())

        selling_auction_page.first_auction_enter_edit_description()

        Assert.contains(registered_domains_page._second_domain_text_value, selling_auction_page.get_page_source())
        Assert.contains(str(selling_auction_page._edit_auction_details_price_start_value), selling_auction_page.get_page_source())

        selling_auction_page.edit_auction_description()

        Assert.contains(u"Zmiany wykonano poprawnie", selling_auction_page.get_page_source())
        Assert.contains(u"\u017b\u0105dane zmiany zosta\u0142y wykonane poprawnie.", selling_auction_page.get_page_source())
        Assert.contains(u"Mo\u017cesz zobaczy\u0107 swoj\u0105 aukcj\u0119 klikaj\u0105c przycisk poni\u017cej.", selling_auction_page.get_page_source())
        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.delete_first_auction()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._second_stage_text_field, u"Aukcja zostanie anulowana"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.second_stage_domain_text())
        WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable(selling_auction_page._submit_button))

        selling_auction_page.delete_auction_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Aukcja została anulowana"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

        selling_auction_page.back_from_results_page()

        self.not_contains(registered_domains_page._second_domain_text_value, selling_auction_page.get_page_source())


#Błąd podczas wykonywania operacji

    def test_sell_on_escrow_auction_should_succeed(self):

        login_value = "alfa"
        price = get_random_integer(2)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.sell_on_escrow_auction(login_value, price)

        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.sell_on_auction_stage2_domain_text())
        Assert.contains(price, registered_domains_page.get_page_source())
        Assert.equal(login_value, registered_domains_page.sell_on_escrow_auction_stage2_buyer_login_text())

        registered_domains_page.sell_on_escrow_auction_stage2()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._add_escrow_transaction_result_text_field, u"Transakcja escrow została rozpoczęta."))

        escrow_auction_page = account_page.header.open_escrow_transactions_seller_list()

        Assert.equal(registered_domains_page._second_domain_text_value, escrow_auction_page.first_auction_domain_name_text())
        Assert.contains(price, escrow_auction_page.get_page_source())
        Assert.equal(login_value, escrow_auction_page.first_auction_buyer_login_text())

        escrow_auction_page.delete_first_escrow_auction()

        Assert.equal(registered_domains_page._second_domain_text_value, escrow_auction_page.delete_auction_domain_name_text())
        Assert.contains(price, escrow_auction_page.get_page_source())
        Assert.equal(login_value, escrow_auction_page.delete_auction_buyer_login_text())

        escrow_auction_page.delete_auction_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._add_escrow_transaction_result_text_field, u"Transakcja escrow została anulowana."))

    def test_search_selling_escrow_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        escrow_auction_page = account_page.header.open_escrow_transactions_seller_list()
        escrow_auction_page.get_text_second_domain_login_and_price()
        escrow_auction_page.search_for_auction(escrow_auction_page.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_auction_page._first_auction_domain_name_field, escrow_auction_page.second_domain_text))
        Assert.equal(escrow_auction_page.second_domain_login_text, escrow_auction_page.first_auction_buyer_login_text())
        Assert.equal(escrow_auction_page.second_domain_price_text, escrow_auction_page.first_auction_price_text())

    def test_sell_on_escrow_auction_the_same_login_should_succeed(self):

        login_value = USER_BETA
        price = get_random_integer(2)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        registered_domains_page.select_second_domain()
        registered_domains_page.sell_on_escrow_auction(login_value, price)

        Assert.contains(registered_domains_page._second_domain_text_value, registered_domains_page.get_page_source())
        Assert.contains(price, registered_domains_page.get_page_source())
        Assert.contains(login_value, registered_domains_page.get_page_source())
        Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", registered_domains_page.get_page_source())

    def test_search_buyer_escrow_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        escrow_auction_page = account_page.header.open_escrow_transactions_buyer_list()
        escrow_auction_page.get_text_second_domain_status_and_price()
        escrow_auction_page.search_for_auction(escrow_auction_page.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_auction_page._first_auction_domain_name_field, escrow_auction_page.second_domain_text))
        Assert.equal(escrow_auction_page.second_domain_status_text, escrow_auction_page.first_auction_buyer_status_text())
        Assert.equal(escrow_auction_page.second_domain_price_text, escrow_auction_page.first_auction_price_text())

    def test_add_on_marketplace_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.fourth_domain_text()
        registered_domains_page.select_fourth_domain()
        registered_domains_page.add_on_marketplace()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Cena Kup Teraz: "+registered_domains_page._add_on_marketplace_buynow_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Cena minimalna: "+registered_domains_page._add_on_marketplace_minimum_price_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Dzierżawa: "+registered_domains_page._add_on_marketplace_lease_value))
        Assert.equal(registered_domains_page._fourth_domain_text_value, registered_domains_page.result_domain_text())

    def test_delete_domain_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.fourth_domain_text()
        registered_domains_page.select_fourth_domain()
        registered_domains_page.delete_auction()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, registered_domains_page.result_domain_text())

    def test_transfer_domain_to_the_same_account_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.fourth_domain_text()
        registered_domains_page.select_fourth_domain()
        registered_domains_page.get_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))

        registered_domains_page.store_authinfo()
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain(registered_domains_page._fourth_domain_text_value, registered_domains_page._authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena już znajduje się na twoim koncie"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, transfer_domain_page.stage2_domain_text())

    def test_transfer_domain_to_the_other_account_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.fourth_domain_text()
        registered_domains_page.select_fourth_domain()
        registered_domains_page.get_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))

        registered_domains_page.store_authinfo()
        account_page = home_page.header.logout()
        account_page = home_page.header.login(USER, PASSWORD)
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain(registered_domains_page._fourth_domain_text_value, registered_domains_page._authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena zostanie przeniesiona z innego konta"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, transfer_domain_page.stage2_domain_text())

        transfer_domain_page.stage2_change_dns_servers()
        transfer_domain_page.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer domeny został zainicjowany"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.cancel_first_domain_transfer()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Transfer zostanie anulowany"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, transfer_domain_page.stage2_domain_text())

        transfer_domain_page.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer został anulowany"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()

        self.not_contains(registered_domains_page._fourth_domain_text_value, transfer_domain_page.get_page_source())

    def test_transfer_domain_to_the_other_account_and_renew_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.fourth_domain_text()
        registered_domains_page.select_fourth_domain()
        registered_domains_page.get_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Kod AuthInfo:"))

        registered_domains_page.store_authinfo()
        account_page = home_page.header.logout()
        account_page = home_page.header.login(USER, PASSWORD)
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain_and_renew(registered_domains_page._fourth_domain_text_value, registered_domains_page._authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena zostanie przeniesiona z innego konta"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, transfer_domain_page.stage2_domain_text())

        transfer_domain_page.stage2_change_dns_servers()
        transfer_domain_page.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer domeny został zainicjowany"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.cancel_first_domain_transfer()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Transfer zostanie anulowany"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, transfer_domain_page.stage2_domain_text())

        transfer_domain_page.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Transfer został anulowany"))
        Assert.equal(registered_domains_page._fourth_domain_text_value, registered_domains_page.result_domain_text())

        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()

        self.not_contains(registered_domains_page._fourth_domain_text_value, transfer_domain_page.get_page_source())

    def test_transfer_domain_to_the_other_account_wrong_data_should_succeed(self):

        _wrong_domain = get_random_uuid(10)+".waw.pl"
        # _wrong_domain = "onet.pl"
        _wrong_authinfo = get_random_uuid(10)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        transfer_domain_page = account_page.header.open_transfer_domain_to_account_list()
        transfer_domain_page.transfer_domain(_wrong_domain, _wrong_authinfo)

        sleep(10)
        if u"Niepoprawny kod AuthInfo: %s" % _wrong_domain in transfer_domain_page.stage2_result_text():
            Assert.equal(_wrong_domain, transfer_domain_page.stage2_domain_text())
        else:
            WebDriverWait(self.driver, 20).until(EC.text_to_be_present_in_element(transfer_domain_page._stage2_result_field, u"Domena nie istnieje"))
            Assert.equal(_wrong_domain, transfer_domain_page.stage2_domain_text())

    def test_add_profile_for_domain_registration_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        profile_list_page = account_page.header.open_profile_for_domain_registration_list()
        profile_list_page.register_new_profile()

        Assert.contains(u"Operacja wykonana poprawnie.", profile_list_page.get_page_source())
        sleep(7)
        Assert.contains(profile_list_page._profile_name_value, profile_list_page.get_page_source())

        profile_list_page.delete_added_profile()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(profile_list_page._result_text_field, u"Operacja wykonana poprawnie"))

        profile_list_page.back_from_results_page()

        self.not_contains(profile_list_page._profile_name_value, profile_list_page.get_page_source())

    def test_search_expired_options_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        expired_options_page = account_page.header.open_expired_options_list()
        expired_options_page.get_text_sixth_option()
        expired_options_page.search_for_option(expired_options_page.sixth_option_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expired_options_page._first_option_value, expired_options_page.sixth_option_text))

#NIE DZIAŁA WYSZUKIWARKA, zgłoszone

    def test_register_option_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.second_domain_text()
        register_option_page = account_page.header.open_register_option_page()
        register_option_page.enter_option_to_register(registered_domains_page._second_domain_text_value)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(register_option_page._stage2_result_field, u"Dostępna do rejestracji"))
        Assert.equal(registered_domains_page._second_domain_text_value, register_option_page.stage2_domain_text())

        register_option_page.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja zawieszona, oczekuje na aktywowanie"))
        Assert.equal(registered_domains_page._second_domain_text_value, registered_domains_page.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, registered_domains_page._second_domain_text_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Rejestracja opcji"))

        to_pay_list.remove_first_payment()

        self.not_contains(registered_domains_page._second_domain_text_value, to_pay_list.get_page_source())
        self.not_contains(u"Rejestracja opcji", to_pay_list.get_page_source())

    def test_register_option_unavailable_should_succeed(self):

        _unavailable_option = get_random_uuid(8)+".unavailable.pl"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        register_option_page = account_page.header.open_register_option_page()
        register_option_page.enter_option_to_register(_unavailable_option)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(register_option_page._stage2_result_field, u"Niedostępna"))
        Assert.equal(_unavailable_option, register_option_page.stage2_domain_text())

    def test_change_option_profile_data_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.first_option_text()
        registered_options_list.change_option_profile_data()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.result_domain_text())

    def test_get_option_authinfo_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.second_option_text()
        registered_options_list.get_option_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Kod AuthInfo:"))
        Assert.equal(registered_options_list._second_option_text_value, registered_options_list.result_domain_text())

    def test_renew_option_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.first_option_text()
        renew_option = registered_options_list.renew_option()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Opcja może być odnowiona"))
        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.stage2_option_text())

        registered_options_list.second_stage_checkboxes_and_submit()

        sleep(10)
        if u"Operacja zawieszona, oczekuje na aktywowanie" in registered_options_list.result_text():
            Assert.equal(registered_options_list._first_option_text_value, registered_options_list.result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Domena już była odnowiona w ostatnim okresie: "))
            Assert.equal(registered_options_list._first_option_text_value, registered_options_list.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, registered_options_list._first_option_text_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Odnowienie opcji"))

        to_pay_list.remove_first_payment()

        self.not_contains(registered_options_list._first_option_text_value, to_pay_list.get_page_source())
        self.not_contains(u"Odnowienie opcji", to_pay_list.get_page_source())

    def test_transfer_option_from_account_should_succeed(self):
        login = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.first_option_text()
        transfer_option = registered_options_list.transfer_option_from_account()
        registered_options_list.transfer_option_enter_login(login)
        registered_options_list.submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer został zainicjowany"))
        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.result_domain_text())

        account_page.header.open_internal_option_transfer_list()

        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.transfer_list_first_domain_text())
        Assert.contains(u"Oczekujący", registered_options_list.get_page_source())

        registered_options_list.delete_first_transfer()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Transfer zostanie anulowany"))
        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.stage2_option_text())

        registered_options_list.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer został anulowany"))
        Assert.equal(registered_options_list._first_option_text_value, registered_options_list.result_domain_text())

        account_page.header.open_internal_option_transfer_list()

        self.not_contains(registered_options_list._first_option_text_value, registered_options_list.get_page_source())
        self.not_contains(u"Oczekujący", registered_options_list.get_page_source())

    def test_transfer_option_from_account_wrong_login_should_succeed(self):
        wrong_login = get_random_string(10)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.first_option_text()
        transfer_option = registered_options_list.transfer_option_from_account()
        registered_options_list.transfer_option_enter_login(wrong_login)
        registered_options_list.submit()

        Assert.contains(u"Użytkownik o podanym loginie nie istnieje", registered_options_list.get_page_source())
        Assert.contains(wrong_login, registered_options_list.get_page_source())

    def test_transfer_option_to_account_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        registered_options_list = account_page.header.open_registered_options_list()
        registered_options_list.second_option_text()
        registered_options_list.get_option_authinfo()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Kod AuthInfo:"))

        registered_options_list.store_option_authinfo()

        home_page.header.logout()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        transfer_option_list = account_page.header.open_transfer_option_to_account_list()
        transfer_option_list.new_option_transfer(registered_options_list._second_option_text_value, registered_options_list._option_authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Opcja zostanie przeniesiona z innego konta"))
        Assert.equal(registered_options_list._second_option_text_value, registered_options_list.stage2_option_text())

        registered_options_list.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer opcji został zainicjowany"))
        Assert.equal(registered_options_list._second_option_text_value, registered_options_list.result_domain_text())

        account_page.header.open_transfer_option_to_account_list()

        Assert.contains(registered_options_list._second_option_text_value, registered_options_list.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), registered_options_list.get_page_source())
        Assert.contains(u"Oczekujący", registered_options_list.get_page_source())

        transfer_option_list.remove_first_transfer()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._stage2_result_field, u"Transfer zostanie anulowany"))
        Assert.equal(registered_options_list._second_option_text_value, registered_options_list.stage2_option_text())

        registered_options_list.submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_options_list._result_text_field, u"Transfer został anulowany"))
        Assert.equal(registered_options_list._second_option_text_value, registered_options_list.result_domain_text())

        account_page.header.open_transfer_option_to_account_list()

        self.not_contains(registered_options_list._second_option_text_value, registered_options_list.get_page_source())

    def test_transfer_option_to_account_option_unavailable_should_succeed(self):

        _unavailable_option = get_random_uuid(8)+".unavailable.pl"
        _wrong_authinfo = get_random_uuid(8)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        transfer_option_list = account_page.header.open_transfer_option_to_account_list()
        transfer_option_list.new_option_transfer(_unavailable_option, _wrong_authinfo)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(transfer_option_list._stage2_result_field, u"Opcja może być przetransferowana"))
        Assert.equal(_unavailable_option, transfer_option_list.stage2_option_text())

    def test_new_hosting_account_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.new_hosting_account(PASSWORD_DELTA)

        Assert.equal("Pakiet Starter", hosting_account_list.get_text_packet_type_stage_2())
        Assert.equal(hosting_account_list._new_hosting_account_login_value, hosting_account_list.get_text_login_stage_2())

        hosting_account_list.new_hosting_account_stage_2()

        WebDriverWait(self.driver, 90).until(EC.text_to_be_present_in_element(hosting_account_list._new_hosting_account_result_text_field, u"Konto hostingowe zostało utworzone i aktywowane na okres próbny 14 dni."))

        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, hosting_account_list._new_hosting_account_login_value))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Zamówienie serwera"))

        to_pay_list.remove_first_payment()

        self.not_contains(hosting_account_list._new_hosting_account_login_value, to_pay_list.get_page_source())
        self.not_contains(u"Zamówienie serwera", to_pay_list.get_page_source())

    def test_add_domain_to_hosting_account_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        registered_domains_page = account_page.header.open_registered_domains_list()
        registered_domains_page.first_domain_text()
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.add_domains_to_hosting_account()
        hosting_account_list.add_domains_to_hosting_account_stage2(registered_domains_page._first_domain_text_value)

        sleep(10)
        if u"Nie udało się zmienić serwerów DNS" in hosting_account_list.result_text():
 	        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
            Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

        hosting_account_list.back_from_results_page()

        Assert.contains(registered_domains_page._first_domain_text_value, hosting_account_list.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), hosting_account_list.get_page_source())

        hosting_account_list.remove_first_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(registered_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(registered_domains_page._first_domain_text_value, registered_domains_page.result_domain_text())

        hosting_account_list.back_from_results_page()

        self.not_contains(registered_domains_page._first_domain_text_value, hosting_account_list.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), hosting_account_list.get_page_source())

    def test_add_domain_to_hosting_account_wrong_domain_name_should_succeed(self):

        _wrong_domain_name = get_random_string(7)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.add_domains_to_hosting_account()
        hosting_account_list.add_domains_to_hosting_account_stage2(_wrong_domain_name)

        Assert.contains(u"Musisz podać poprawne nazwy domen", hosting_account_list.get_page_source())

    def test_renew_hosting_account_manually_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hosting_account_list = account_page.header.open_hosting_account_list()
        hosting_account_list.first_hosting_account_get_text()
        hosting_account_list.renew_first_hosting_account()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hosting_account_list._stage2_result_text_field, u"Konto hostingowe zostanie przedłużone"))
        Assert.equal(hosting_account_list._first_hosting_account_text, hosting_account_list.stage2_result_domain_text())

        hosting_account_list.renew_hosting_account_stage2()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hosting_account_list._result_text_field, u"Operacja zawieszona, oczekuje na aktywowanie"))
        Assert.equal(hosting_account_list._first_hosting_account_text, hosting_account_list.result_domain_text())

        to_pay_list = account_page.header.open_to_pay_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_title, hosting_account_list._first_hosting_account_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(to_pay_list._first_payment_type, u"Przedłużenie hostingu"))

        to_pay_list.remove_first_payment()

        self.not_contains(hosting_account_list._first_hosting_account_text, to_pay_list.get_page_source())
        self.not_contains(u"Przedłużenie hostingu", to_pay_list.get_page_source())

    def test_add_offer_on_marketplace_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER, PASSWORD)
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.get_text_second_domain()
        domains_on_marketplace_list.add_offer_to_second_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._domain_field_stage1, domains_on_marketplace_list._second_domain_text))

        domains_on_marketplace_list.get_text_price_buynow()
        domains_on_marketplace_list.submit_offer_stage1()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._domain_field_stage1, domains_on_marketplace_list._second_domain_text))
        Assert.contains(domains_on_marketplace_list.price_buynow, domains_on_marketplace_list.get_page_source())
        Assert.contains(domains_on_marketplace_list._price_value, domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.submit_offer_stage2()

        Assert.contains(u"Oferta została złożona", domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.delete_offer_stage1()

        Assert.contains(domains_on_marketplace_list._price_value, domains_on_marketplace_list.get_page_source())
        Assert.contains(domains_on_marketplace_list._second_domain_text, domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.delete_offer_stage2()

# BŁĄD "BRAK DOSTEPU DO OBIEKTU"
# AUTOMATYCZNE WYLOGOWANIE PO add_offer_to_second_domain()

    def test_search_domains_on_marketplace_should_succeed(self):
        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.get_text_fourth_domain_and_price()
        domains_on_marketplace_list.search_for_domain(domains_on_marketplace_list._fourth_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._submit_offer_domain_name_value, domains_on_marketplace_list._fourth_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domains_on_marketplace_list._submit_offer_price_value, domains_on_marketplace_list._fourth_domain_price_text))

    def test_filter_domains_on_marketplace_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.filter_results_12_characters_com_pl()

        Assert.true(re.compile(r"^\w{12}\.com\.pl$").match(domains_on_marketplace_list.first_domain_text()))

    def test_subscribe_filtered_domains_on_marketplace_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        domains_on_marketplace_list = account_page.header.open_domains_on_marketplace_list()
        domains_on_marketplace_list.filter_results_length_com_pl()
        domains_on_marketplace_list.subscribe_results()

        Assert.contains(u"Długość:", domains_on_marketplace_list.get_page_source())
        Assert.contains(str(domains_on_marketplace_list._filter_length_from_value), domains_on_marketplace_list.get_page_source())
        Assert.contains(str(domains_on_marketplace_list._filter_length_to_value), domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.subscribe_results_stage2()

        Assert.contains(domains_on_marketplace_list._subscribe_results_subuscription_name_value, domains_on_marketplace_list.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.delete_first_subscription()

        Assert.contains(domains_on_marketplace_list._subscribe_results_subuscription_name_value, domains_on_marketplace_list.get_page_source())
        Assert.contains(u"Długość:", domains_on_marketplace_list.get_page_source())
        Assert.contains(str(domains_on_marketplace_list._filter_length_from_value), domains_on_marketplace_list.get_page_source())
        Assert.contains(str(domains_on_marketplace_list._filter_length_to_value), domains_on_marketplace_list.get_page_source())

        domains_on_marketplace_list.delete_subscription_stage2()

        Assert.contains(u"Operacja wykonana poprawnie.", domains_on_marketplace_list.get_page_source())
        sleep(7)
        Assert.contains(u"Brak subskrypcji domen na giełdzie", domains_on_marketplace_list.get_page_source())
        self.not_contains(domains_on_marketplace_list._subscribe_results_subuscription_name_value, domains_on_marketplace_list.get_page_source())

    def test_watch_new_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        watched_domains_page = account_page.header.open_watched_domains_list()
        watched_domains_page.watch_new_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(watched_domains_page._domain_name_value, watched_domains_page.result_domain_text())

        account_page.header.open_watched_domains_list()

        Assert.contains(watched_domains_page._domain_name_value, watched_domains_page.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), watched_domains_page.get_page_source())

        watched_domains_page.first_domain_change_watch_settings()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(watched_domains_page._domain_name_value, watched_domains_page.result_domain_text())

        account_page.header.open_watched_domains_list()
        watched_domains_page.delete_first_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_domains_page._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(watched_domains_page._domain_name_value, watched_domains_page.result_domain_text())

        watched_domains_page.back_from_results_page()

        self.not_contains(watched_domains_page._domain_name_value, watched_domains_page.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), watched_domains_page.get_page_source())

    def test_watch_new_seller_should_succeed(self):

        seller_name = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        watched_sellers_page = account_page.header.open_watched_sellers_list()
        watched_sellers_page.watch_new_seller(seller_name)

        Assert.contains(seller_name, watched_sellers_page.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), watched_sellers_page.get_page_source())

        watched_sellers_page.change_first_seller_settings()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_sellers_page._result_text_field, u"Operacja wykonana poprawnie"))

        account_page.header.open_watched_sellers_list()
        watched_sellers_page.delete_first_seller()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(watched_sellers_page._result_text_field, u"Operacja wykonana poprawnie"))

        watched_sellers_page.back_from_results_page()

        self.not_contains(seller_name, watched_sellers_page.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), watched_sellers_page.get_page_source())

    def test_watch_new_seller_the_same_login_should_succeed(self):

        seller_name = USER_DELTA

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        watched_sellers_page = account_page.header.open_watched_sellers_list()
        watched_sellers_page.watch_new_seller(seller_name)

        Assert.contains(u"Nie możesz obserwować samego siebie", watched_sellers_page.get_page_source())

    def test_new_option_auction_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        new_option_auction_page = account_page.header.open_new_option_auction_page()
        new_option_auction_page.new_option_auction_enter_details()

        Assert.contains(new_option_auction_page._option_name, new_option_auction_page.get_page_source())
        Assert.contains(str(new_option_auction_page._price_start_value), new_option_auction_page.get_page_source())
        Assert.contains(str(new_option_auction_page._price_minimum_value), new_option_auction_page.get_page_source())
        Assert.contains(str(new_option_auction_page._price_buynow_value), new_option_auction_page.get_page_source())
        Assert.contains(new_option_auction_page._description_value, new_option_auction_page.get_page_source())

        new_option_auction_page.new_option_auction_stage_2_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(new_option_auction_page._result_text_field, u"Aukcja została wystawiona"))
        Assert.equal(new_option_auction_page._option_name, new_option_auction_page.result_domain_text())

        selling_auction_page = account_page.header.open_selling_auction_list()
        selling_auction_page.delete_first_auction()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(new_option_auction_page._stage2_result_text_field, u"Aukcja zostanie anulowana"))
        Assert.equal(new_option_auction_page._option_name, new_option_auction_page.stage2_result_domain_text())

        selling_auction_page.delete_auction_submit()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(new_option_auction_page._result_text_field, u"Aukcja została anulowana"))
        Assert.equal(new_option_auction_page._option_name, new_option_auction_page.result_domain_text())

        selling_auction_page.back_from_results_page()

        self.not_contains(new_option_auction_page._option_name, selling_auction_page.get_page_source())

    def test_search_seller_ended_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        ended_auctions_list = account_page.header.open_seller_ended_auctions_list()
        ended_auctions_list.get_second_domain_and_price_text()
        ended_auctions_list.search_for_domain(ended_auctions_list._second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_checkbox, ended_auctions_list._second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_price_field, ended_auctions_list._second_domain_price_text))

    def test_search_buyer_ended_auctions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        ended_auctions_list = account_page.header.open_buyer_ended_auctions_list()
        ended_auctions_list.get_second_domain_and_price_text()
        ended_auctions_list.search_for_domain(ended_auctions_list._second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_checkbox, ended_auctions_list._second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(ended_auctions_list._first_domain_price_field, ended_auctions_list._second_domain_price_text))

    def test_new_escrow_option_transaction_should_succeed(self):

        login = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        escrow_option_transaction_page = account_page.header.open_escrow_option_selling_transaction_list()
        escrow_option_transaction_page.add_escrow_option_transaction(login)

        Assert.equal(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.stage2_option_text())
        Assert.equal(login, escrow_option_transaction_page.stage2_login_text())
        Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())

        escrow_option_transaction_page.add_description()
        escrow_option_transaction_page.stage2_submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._added_transaction_result_text_field, u"Transakcja escrow została rozpoczęta."))

        account_page.header.open_escrow_option_selling_transaction_list()

        Assert.contains(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.get_page_source())
        Assert.contains(login, escrow_option_transaction_page.get_page_source())
        Assert.contains("Nowa", escrow_option_transaction_page.get_page_source())
        Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())

        escrow_option_transaction_page.delete_first_auction()

        Assert.equal(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.stage2_option_text())
        Assert.equal(login, escrow_option_transaction_page.stage2_login_text())
        Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())

        escrow_option_transaction_page.stage2_submit_and_accept_alert()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._added_transaction_result_text_field, u"Transakcja escrow została anulowana."))

        account_page.header.open_escrow_option_selling_transaction_list()
        escrow_option_transaction_page.filter_new()

        self.not_contains(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.get_page_source())
        self.not_contains(login, escrow_option_transaction_page.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), escrow_option_transaction_page.get_page_source())

    def test_search_escrow_option_selling_transactions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        escrow_option_transaction_page = account_page.header.open_escrow_option_selling_transaction_list()
        escrow_option_transaction_page.get_text_third_domain_login_and_price()
        escrow_option_transaction_page.search_for_auction(escrow_option_transaction_page.third_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_field, escrow_option_transaction_page.third_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_login_field, escrow_option_transaction_page.third_domain_login_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_price_field, escrow_option_transaction_page.third_domain_price_text))

    def test_new_escrow_option_transaction_the_same_login_should_succeed(self):

        login = USER_BETA

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        escrow_option_transaction_page = account_page.header.open_escrow_option_selling_transaction_list()
        escrow_option_transaction_page.add_escrow_option_transaction(login)

        Assert.contains(escrow_option_transaction_page._first_option_text_value, escrow_option_transaction_page.get_page_source())
        Assert.contains(login, escrow_option_transaction_page.get_page_source())
        Assert.contains(escrow_option_transaction_page._price_value, escrow_option_transaction_page.get_page_source())
        Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", escrow_option_transaction_page.get_page_source())

    def test_search_escrow_option_buying_transactions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        escrow_option_transaction_page = account_page.header.open_escrow_option_buying_transaction_list()
        escrow_option_transaction_page.get_text_second_domain_status_and_price()
        escrow_option_transaction_page.search_for_auction(escrow_option_transaction_page.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_field, escrow_option_transaction_page.second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_status_field, escrow_option_transaction_page.second_domain_status_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(escrow_option_transaction_page._first_domain_price_field, escrow_option_transaction_page.second_domain_price_text))

    def test_search_rental_buyer_transactions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_buyer_list = account_page.header.open_rental_buyer_list()
        rental_buyer_list.get_text_second_domain_status_and_price()
        rental_buyer_list.search_for_domain(rental_buyer_list.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_buyer_list._first_domain_field, rental_buyer_list.second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_buyer_list._first_domain_status_field, rental_buyer_list.second_domain_status_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_buyer_list._first_domain_price_field, rental_buyer_list.second_domain_price_text))

    def test_rental_buyer_transaction_details_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_buyer_list = account_page.header.open_rental_buyer_list()
        rental_buyer_list.get_text_second_domain_status_and_price()
        rental_buyer_list.enter_second_domain_details()

        Assert.contains(rental_buyer_list.second_domain_text, rental_buyer_list.get_page_source())
        Assert.contains(rental_buyer_list.second_domain_price_text, rental_buyer_list.get_page_source())

    def test_rental_buyer_transaction_add_note_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_buyer_list = account_page.header.open_rental_buyer_list()
        rental_buyer_list.get_text_second_domain_status_and_price()
        rental_buyer_list.second_domain_enter_add_note()

        Assert.contains(rental_buyer_list.second_domain_text, rental_buyer_list.get_page_source())

        rental_buyer_list.add_note()
        rental_buyer_list.second_domain_enter_add_note()

        Assert.contains(rental_buyer_list._add_note_value, rental_buyer_list.get_page_source())

    def test_search_rental_seller_transactions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        rental_seller_list = account_page.header.open_rental_seller_list()
        rental_seller_list.get_text_second_domain_login_status_and_price()
        rental_seller_list.search_for_domain(rental_seller_list.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_field, rental_seller_list.second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_login_field, rental_seller_list.second_domain_login_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_status_field, rental_seller_list.second_domain_status_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(rental_seller_list._first_domain_price_field, rental_seller_list.second_domain_price_text))

    def test_rental_seller_transaction_details_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_seller_list = account_page.header.open_rental_seller_list()
        rental_seller_list.get_text_second_domain_login_status_and_price()
        rental_seller_list.enter_second_domain_details()

        Assert.contains(rental_seller_list.second_domain_text, rental_seller_list.get_page_source())
        Assert.contains(rental_seller_list.second_domain_login_text, rental_seller_list.get_page_source())
        Assert.contains(rental_seller_list.second_domain_price_text, rental_seller_list.get_page_source())

    def test_rental_seller_transaction_add_note_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_seller_list = account_page.header.open_rental_seller_list()
        rental_seller_list.get_text_second_domain_login_status_and_price()
        rental_seller_list.second_domain_enter_add_note()

        Assert.contains(rental_seller_list.second_domain_text, rental_seller_list.get_page_source())
        Assert.contains(rental_seller_list.second_domain_login_text, rental_seller_list.get_page_source())

        rental_seller_list.add_note()
        rental_seller_list.second_domain_enter_add_note()

        Assert.contains(rental_seller_list._add_note_value, rental_seller_list.get_page_source())

    def test_new_rental_seller_transaction_should_succeed(self):

        login= "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        rental_seller_list = account_page.header.open_rental_seller_list()
        rental_seller_list.add_rental_transaction(login)

        Assert.contains(rental_seller_list._rental_domain_name_text, rental_seller_list.get_page_source())
        Assert.contains(login, rental_seller_list.get_page_source())
        Assert.contains(rental_seller_list._add_rental_transaction_monthly_rent_value, rental_seller_list.get_page_source())
        Assert.contains(str(rental_seller_list._add_rental_transaction_rent_duration_value)+" miesi", rental_seller_list.get_page_source())
        Assert.contains(u"Wydzierżawiający może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
        Assert.contains(u"Dzierżawca może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
        Assert.contains(str(rental_seller_list._add_rental_transaction_notice_period_value)+" miesi", rental_seller_list.get_page_source())
        Assert.contains(str(rental_seller_list._add_rental_transaction_preemption_price_value), rental_seller_list.get_page_source())

        rental_seller_list.add_rental_transaction_submit()
        account_page.header.open_rental_seller_list()

        Assert.contains(rental_seller_list._rental_domain_name_text, rental_seller_list.get_page_source())
        Assert.contains(login, rental_seller_list.get_page_source())
        Assert.contains(rental_seller_list._add_rental_transaction_monthly_rent_value, rental_seller_list.get_page_source())

        rental_seller_list.cancel_first_rental_transaction()

        Assert.contains(rental_seller_list._rental_domain_name_text, rental_seller_list.get_page_source())
        Assert.contains(login, rental_seller_list.get_page_source())
        Assert.contains(rental_seller_list._add_rental_transaction_monthly_rent_value, rental_seller_list.get_page_source())
        Assert.contains(str(rental_seller_list._add_rental_transaction_rent_duration_value)+" miesi", rental_seller_list.get_page_source())
        Assert.contains(u"Wydzierżawiający może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
        Assert.contains(u"Dzierżawca może wypowiedzieć dzierżawę", rental_seller_list.get_page_source())
        Assert.contains(str(rental_seller_list._add_rental_transaction_notice_period_value)+" miesi", rental_seller_list.get_page_source())
        Assert.contains(str(rental_seller_list._add_rental_transaction_preemption_price_value), rental_seller_list.get_page_source())

        rental_seller_list.cancel_first_rental_transaction_submit()

        Assert.contains(u"Transakcja dzierżawy została anulowana.", rental_seller_list.get_page_source())

    def test_new_rental_seller_transaction_wrong_login_should_succeed(self):

        login= get_random_string(10)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_seller_list = account_page.header.open_rental_seller_list()
        rental_seller_list.add_rental_transaction(login)

        Assert.contains(u"Użytkownik o podanym loginie nie istnieje", rental_seller_list.get_page_source())

    def test_new_rental_seller_transaction_the_same_login_should_succeed(self):

        login = USER_DELTA

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_seller_list = account_page.header.open_rental_seller_list()
        rental_seller_list.add_rental_transaction(login)

        Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", rental_seller_list.get_page_source())

    def test_new_rental_seller_transaction_wrong_domain_name_should_succeed(self):

        login = "alfa"
        domain_name = get_random_string(10)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        rental_seller_list = account_page.header.open_rental_seller_list()
        rental_seller_list.add_rental_transaction_wrong_domain_name(login, domain_name)

        Assert.contains(u"Domena nie jest zarejestrowana", rental_seller_list.get_page_source())

    def test_search_hire_buyer_transactions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_buyer_list = account_page.header.open_hire_buyer_list()
        hire_buyer_list.get_text_second_domain_status_price_and_installments()
        hire_buyer_list.search_for_domain(hire_buyer_list.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_field, hire_buyer_list.second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_status_field, hire_buyer_list.second_domain_status_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_price_field, hire_buyer_list.second_domain_price_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_buyer_list._first_domain_installments_field, hire_buyer_list.second_domain_installments_text))

    def test_hire_buyer_transaction_details_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_buyer_list = account_page.header.open_hire_buyer_list()
        hire_buyer_list.get_text_second_domain_status_price_and_installments()
        hire_buyer_list.enter_second_domain_details()

        Assert.contains(hire_buyer_list.second_domain_text, hire_buyer_list.get_page_source())
        Assert.contains(hire_buyer_list.second_domain_price_text, hire_buyer_list.get_page_source())
        Assert.contains(hire_buyer_list.second_domain_installments_text, hire_buyer_list.get_page_source())

    def test_hire_buyer_transaction_add_note_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_buyer_list = account_page.header.open_hire_buyer_list()
        hire_buyer_list.get_text_second_domain_status_price_and_installments()
        hire_buyer_list.second_domain_enter_add_note()

        Assert.contains(hire_buyer_list.second_domain_text, hire_buyer_list.get_page_source())

        hire_buyer_list.add_note()
        hire_buyer_list.second_domain_enter_add_note()

        Assert.contains(hire_buyer_list._add_note_value, hire_buyer_list.get_page_source())

    def test_search_hire_seller_transactions_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        hire_seller_list = account_page.header.open_hire_seller_list()
        hire_seller_list.get_text_second_domain_login_status_price_and_installments()
        hire_seller_list.search_for_domain(hire_seller_list.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_field, hire_seller_list.second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_login_field, hire_seller_list.second_domain_login_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_status_field, hire_seller_list.second_domain_status_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_price_field, hire_seller_list.second_domain_price_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._first_domain_installments_field, hire_seller_list.second_domain_installments_text))

    def test_hire_seller_transaction_details_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_seller_list = account_page.header.open_hire_seller_list()
        hire_seller_list.get_text_second_domain_login_status_price_and_installments()
        hire_seller_list.enter_second_domain_details()

        Assert.contains(hire_seller_list.second_domain_text, hire_seller_list.get_page_source())
        Assert.contains(hire_seller_list.second_domain_login_text, hire_seller_list.get_page_source())
        Assert.contains(hire_seller_list.second_domain_price_text, hire_seller_list.get_page_source())
        Assert.contains(hire_seller_list.second_domain_installments_text, hire_seller_list.get_page_source())

    def test_hire_seller_transaction_add_note_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_seller_list = account_page.header.open_hire_seller_list()
        hire_seller_list.get_text_second_domain_login_status_price_and_installments()
        hire_seller_list.second_domain_enter_add_note()

        Assert.contains(hire_seller_list.second_domain_text, hire_seller_list.get_page_source())
        Assert.contains(hire_seller_list.second_domain_login_text, hire_seller_list.get_page_source())

        hire_seller_list.add_note()
        hire_seller_list.second_domain_enter_add_note()

        Assert.contains(hire_seller_list._add_note_value, hire_seller_list.get_page_source())

    def test_new_hire_seller_transaction_should_succeed(self):

        login = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_seller_list = account_page.header.open_hire_seller_list()
        hire_seller_list.add_hire_transaction_stage1()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._add_hire_transaction_domain_name_second_checkbox, ".pl"))

        hire_seller_list.add_hire_transaction_stage2(login)

        Assert.contains(hire_seller_list._hire_domain_name_text, hire_seller_list.get_page_source())
        Assert.contains(login, hire_seller_list.get_page_source())
        Assert.contains(hire_seller_list._add_hire_transaction_monthly_installment_value, hire_seller_list.get_page_source())
        Assert.contains(str(hire_seller_list._add_hire_transaction_number_of_installments_value)+" miesi", hire_seller_list.get_page_source())
        Assert.contains(str(int(hire_seller_list._add_hire_transaction_monthly_installment_value) * int(hire_seller_list._add_hire_transaction_number_of_installments_value)), hire_seller_list.get_page_source())

        hire_seller_list.add_hire_transaction_submit()
        account_page.header.open_hire_seller_list()

        Assert.contains(hire_seller_list._hire_domain_name_text, hire_seller_list.get_page_source())
        Assert.contains(login, hire_seller_list.get_page_source())
        Assert.contains(str(int(hire_seller_list._add_hire_transaction_monthly_installment_value) * int(hire_seller_list._add_hire_transaction_number_of_installments_value)), hire_seller_list.get_page_source())

        hire_seller_list.cancel_first_hire_transaction()

        Assert.contains(hire_seller_list._hire_domain_name_text, hire_seller_list.get_page_source())
        Assert.contains(login, hire_seller_list.get_page_source())
        Assert.contains(hire_seller_list._add_hire_transaction_monthly_installment_value, hire_seller_list.get_page_source())
        Assert.contains(str(hire_seller_list._add_hire_transaction_number_of_installments_value)+" miesi", hire_seller_list.get_page_source())
        Assert.contains(str(int(hire_seller_list._add_hire_transaction_monthly_installment_value) * int(hire_seller_list._add_hire_transaction_number_of_installments_value)), hire_seller_list.get_page_source())

        hire_seller_list.cancel_first_hire_transaction_submit()

        Assert.contains(u"Transakcja sprzedaży na raty została anulowana.", hire_seller_list.get_page_source())

    def test_new_hire_seller_transaction_wrong_login_should_succeed(self):

        login = get_random_string(9)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_seller_list = account_page.header.open_hire_seller_list()
        hire_seller_list.add_hire_transaction_stage1()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._add_hire_transaction_domain_name_second_checkbox, ".pl"))

        hire_seller_list.add_hire_transaction_stage2(login)

        Assert.contains(u"Użytkownik o podanym loginie nie istnieje", hire_seller_list.get_page_source())

    def test_new_hire_seller_transaction_the_same_login_should_succeed(self):

        login = USER_DELTA

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_seller_list = account_page.header.open_hire_seller_list()
        hire_seller_list.add_hire_transaction_stage1()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(hire_seller_list._add_hire_transaction_domain_name_second_checkbox, ".pl"))

        hire_seller_list.add_hire_transaction_stage2(login)

        Assert.contains(u"Nie możesz przeprowadzić transakcji sam ze sobą", hire_seller_list.get_page_source())

    def test_new_hire_seller_transaction_wrong_domain_name_should_succeed(self):

        login = "alfa"
        domain_name = get_random_string(9)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        hire_seller_list = account_page.header.open_hire_seller_list()
        hire_seller_list.add_hire_transaction_wrong_domain_name(login, domain_name)

        Assert.contains(u"Domena nie jest zarejestrowana", hire_seller_list.get_page_source())

    def test_block_seller_should_succeed(self):

        seller_name = "alfa"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        blocked_sellers_page = account_page.header.open_blocked_sellers_list()
        blocked_sellers_page.block_seller(seller_name)

        Assert.contains(u"Operacja wykonana poprawnie.", blocked_sellers_page.get_page_source())
        sleep(7)
        Assert.contains(seller_name, blocked_sellers_page.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), blocked_sellers_page.get_page_source())

        blocked_sellers_page.delete_first_seller()

        Assert.contains(seller_name, blocked_sellers_page.get_page_source())
        Assert.contains(blocked_sellers_page._note_value, blocked_sellers_page.get_page_source())

        blocked_sellers_page.delete_first_seller_submit()

        Assert.contains(u"Operacja wykonana poprawnie.", blocked_sellers_page.get_page_source())
        sleep(7)
        self.not_contains(seller_name, blocked_sellers_page.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), blocked_sellers_page.get_page_source())

    def test_block_seller_wrong_login_should_succeed(self):

        seller_name = get_random_string(10)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        blocked_sellers_page = account_page.header.open_blocked_sellers_list()
        blocked_sellers_page.block_seller(seller_name)

        Assert.contains(seller_name, blocked_sellers_page.get_page_source())
        Assert.contains(u"Użytkownik o podanym loginie nie istnieje", blocked_sellers_page.get_page_source())

    def test_search_selling_history_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        selling_history_page = account_page.header.open_selling_history_list()
        selling_history_page.get_second_domain_text()
        selling_history_page.search_for_domain(selling_history_page._second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(selling_history_page._first_domain_checkbox, selling_history_page._second_domain_text))

    def test_catch_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        expiring_domains_list = account_page.header.open_expiring_domains_list()
        expiring_domains_list.first_domain_text()
        expiring_domains_list.catch_first_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expiring_domains_list._result_text_field, u"Domena dodana do przechwycenia"))
        Assert.equal(expiring_domains_list._first_domain_text_value, expiring_domains_list.result_domain_text())

        domains_to_catch = account_page.header.open_domains_to_catch_list()

        Assert.contains(expiring_domains_list._first_domain_text_value, domains_to_catch.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), domains_to_catch.get_page_source())

        domains_to_catch.delete_first_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expiring_domains_list._result_text_field, u"Operacja wykonana poprawnie"))
        Assert.equal(expiring_domains_list._first_domain_text_value, expiring_domains_list.result_domain_text())

        account_page.header.open_domains_to_catch_list()

        self.not_contains(expiring_domains_list._first_domain_text_value, domains_to_catch.get_page_source())
        self.not_contains(strftime("%Y-%m-%d", gmtime()), domains_to_catch.get_page_source())

    def test_search_domains_to_catch_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        expiring_domains_list = account_page.header.open_expiring_domains_list()
        expiring_domains_list.sixth_domain_text()
        expiring_domains_list.search_for_domain_to_catch(expiring_domains_list._sixth_domain_text_value)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(expiring_domains_list._first_domain_checkbox, expiring_domains_list._sixth_domain_text_value))

    def test_filter_domains_to_catch_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        expiring_domains_list = account_page.header.open_expiring_domains_list()
        expiring_domains_list.filter_results_4_characters_com_pl()

        Assert.true(re.compile(r"^\w{4}\.com\.pl$").match(expiring_domains_list.first_domain_text()))

    def test_subscribe_filtered_domains_to_catch_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_BETA, PASSWORD_BETA)
        expiring_domains_list = account_page.header.open_expiring_domains_list()
        expiring_domains_list.filter_results_length_and_pl()
        expiring_domains_list.subscribe_results()

        Assert.contains("Rozszerzenie:", expiring_domains_list.get_page_source())
        Assert.contains(".pl", expiring_domains_list.get_page_source())
        Assert.contains(u"Długość:", expiring_domains_list.get_page_source())
        Assert.contains(str(expiring_domains_list._filter_length_from_value), expiring_domains_list.get_page_source())
        Assert.contains(str(expiring_domains_list._filter_length_to_value), expiring_domains_list.get_page_source())

        expiring_domains_list.enter_subscription_name_and_submit()
        subscriptions_list = account_page.header.open_expiring_domains_subscriptions_list()

        Assert.contains(expiring_domains_list._subscription_name_value, expiring_domains_list.get_page_source())
        Assert.contains(strftime("%Y-%m-%d", gmtime()), expiring_domains_list.get_page_source())

        expiring_domains_list.delete_added_subscription_1_stage()

        Assert.contains(expiring_domains_list._subscription_name_value, expiring_domains_list.get_page_source())
        Assert.contains("Rozszerzenie:", expiring_domains_list.get_page_source())
        Assert.contains(".pl", expiring_domains_list.get_page_source())
        Assert.contains(u"Długość:", expiring_domains_list.get_page_source())
        Assert.contains(str(expiring_domains_list._filter_length_from_value), expiring_domains_list.get_page_source())
        Assert.contains(str(expiring_domains_list._filter_length_to_value), expiring_domains_list.get_page_source())

        expiring_domains_list.delete_added_subscription_2_stage()

        self.not_contains(expiring_domains_list._subscription_name_value, expiring_domains_list.get_page_source())

# DO SPRAWDZENIA BO BŁĄD PRZY DWUKROTNYM DODAWANIU SUBSKRYPCJI

    def test_search_monitor_domains_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        monitor_domains_list = account_page.header.open_monitor_domains_list()
        monitor_domains_list.get_text_second_domain_and_status()
        monitor_domains_list.search_for_domain(monitor_domains_list.second_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_field, monitor_domains_list.second_domain_text))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_status_field, monitor_domains_list.second_domain_status_text))

    def test_change_first_monitored_domain_settings_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        monitor_domains_list = account_page.header.open_monitor_domains_list()
        monitor_domains_list.get_text_first_domain()
        monitor_domains_list.change_first_domain_settings()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Opcje monitorowania zmienione"))
        Assert.equal(monitor_domains_list.first_domain_text, monitor_domains_list.result_domain_text())

    def test_monitor_new_domain_should_succeed(self):

        domain_name = "aaaaaa"+get_random_string(6)+".waw.pl"

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        monitor_domains_list = account_page.header.open_monitor_domains_list()
        monitor_domains_list.monitor_new_domain(domain_name)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Monitorowanie domeny włączone"))
        Assert.equal(domain_name, monitor_domains_list.result_domain_text())

        account_page.header.open_monitor_domains_list()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_field, domain_name))

        monitor_domains_list.remove_first_monitored_domain()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Monitorowanie domeny wyłączone"))
        Assert.equal(domain_name, monitor_domains_list.result_domain_text())

        account_page.header.open_monitor_domains_list()

        self.not_contains(domain_name, monitor_domains_list.get_page_source())

    def test_monitor_new_domain_already_monitored_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        monitor_domains_list = account_page.header.open_monitor_domains_list()
        monitor_domains_list.get_text_first_domain()
        monitor_domains_list.monitor_new_domain(monitor_domains_list.first_domain_text)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._result_text_field, u"Już monitorujesz tę domenę"))
        Assert.equal(monitor_domains_list.first_domain_text, monitor_domains_list.result_domain_text())

    def test_filter_monitored_domains_available_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        monitor_domains_list = account_page.header.open_monitor_domains_list()
        monitor_domains_list.filter_available()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_status_field, u"Dostępna"))

    def test_filter_monitored_domains_registered_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        monitor_domains_list = account_page.header.open_monitor_domains_list()
        monitor_domains_list.filter_registered()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(monitor_domains_list._first_domain_status_field, u"Zarejestrowana"))

    def test_add_domain_catalog_should_succeed(self):

        catalog_name = "aaaaaaaa"+get_random_string(5)

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        domain_catalog_list = account_page.header.open_domain_catalog_list()
        domain_catalog_list.add_catalog_stage1(catalog_name)

        Assert.contains(catalog_name, domain_catalog_list.get_page_source())

        domain_catalog_list.add_catalog_stage2()

        sleep(10)
        if u"Domena nie jest wystawiona na sprzedaż" in domain_catalog_list.result_text():
            Assert.equal(domain_catalog_list.domain_name, domain_catalog_list.result_domain_text())
        else:
            WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._result_text_field, u"Domena dodana do katalogu"))
            Assert.equal(domain_catalog_list.domain_name, domain_catalog_list.result_domain_text())

        domain_catalog_list.back_to_domains_in_catalog()

        Assert.contains(domain_catalog_list.domain_name, domain_catalog_list.get_page_source())

        domain_catalog_list.remove_first_domain_in_catalog()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._result_text_field, u"Domena usunięta z katalogu"))
        Assert.equal(domain_catalog_list.domain_name, domain_catalog_list.result_domain_text())

        domain_catalog_list.back_to_domains_in_catalog()

        self.not_contains(domain_catalog_list.domain_name, domain_catalog_list.get_page_source())

        account_page.header.open_domain_catalog_list()

        domain_catalog_list.remove_first_catalog()

        sleep(2)
        Assert.contains(u"Operacja wykonana poprawnie.", domain_catalog_list.get_page_source())

        sleep(7)
        self.not_contains(catalog_name, domain_catalog_list.get_page_source())

    def test_add_domain_to_catalog_already_added_domain_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        domain_catalog_list = account_page.header.open_domain_catalog_list()
        domain_catalog_list.add_already_existing_domain_to_catalog()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._result_text_field, u"Domena już znajduje się w katalogu"))
        Assert.equal(domain_catalog_list.first_domain_value, domain_catalog_list.result_domain_text())

    def test_search_domain_in_catalog_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_GAMMA, PASSWORD_GAMMA)
        domain_catalog_list = account_page.header.open_domain_catalog_list()
        domain_catalog_list.search_second_domain_in_catalog()

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(domain_catalog_list._first_domain_in_catalog_field, domain_catalog_list.second_domain_value))

    def test_search_appraisal_list_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        appraisal_list = account_page.header.open_appraisal_list()
        appraisal_list.get_fourth_appraisal_domain_time_type_and_status()
        appraisal_list.search_for_appraisal(appraisal_list.fourth_appraisal_domain)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_domain_field, appraisal_list.fourth_appraisal_domain))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_time_field, appraisal_list.fourth_appraisal_time))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_type_field, appraisal_list.fourth_appraisal_type))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_status_field, appraisal_list.fourth_appraisal_status))

#BŁĄD BRAK WYNIKÓW

    def test_search_active_appraisals_list_should_succeed(self):

        home_page = HomePage(self.driver).open_home_page()
        account_page = home_page.header.login(USER_DELTA, PASSWORD_DELTA)
        appraisal_list = account_page.header.open_active_appraisals_list()
        appraisal_list.get_fourth_appraisal_domain_time_and_propositions()
        appraisal_list.search_for_appraisal(appraisal_list.fourth_appraisal_domain)

        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_domain_field, appraisal_list.fourth_appraisal_domain))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_time_field, appraisal_list.fourth_appraisal_time))
        WebDriverWait(self.driver, 30).until(EC.text_to_be_present_in_element(appraisal_list._first_appraisal_propositions_field, appraisal_list.fourth_appraisal_propositions))

#BŁĄD BRAK WYNIKÓW

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