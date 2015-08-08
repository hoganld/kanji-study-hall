import unittest

from django.conf import settings

from .functionalbase import FunctionalTest

class RegistrationTest(FunctionalTest):
    """We will be using the django-allauth module, which we don't need to
    test per se, as it has its own tests. These tests are intended to simply
    ensure that we have wired up our urls/templates correctly.

    """

    def test_signup_signin_signout(self):
        # Sherman studies Japanese in his spare time. Sherman's a nerd.
        # He is therefore quite pleased to discover Kanji Study Hall.
        self.browser.get(self.live_server_url)
        self.assertEqual("Kanji Study Hall", self.browser.title)
        # He immediately tries to sign up.
        self.browser.find_element_by_id("id_signup").click()
        # He finds himself filling out a registration form
        username = self.browser.find_element_by_id("id_username")
        password1 = self.browser.find_element_by_id("id_password1")
        password2 = self.browser.find_element_by_id("id_password2")
        username.send_keys("sherman")
        password1.send_keys("password")
        password2.send_keys("password")
        # He submits it
        self.browser.find_element_by_xpath("//button[@type='submit']").click()
        # instead of "sign in" and "sign up" he sees "sign out"
        self.wait_for_element_with_id("id_logout")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertNotIn("Sign in", navbar.text)
        self.assertNotIn("Sign up", navbar.text)
        self.assertIn("Sign out", navbar.text)
        self.browser.find_element_by_id("id_logout").click()
        self.browser.find_element_by_xpath("//button[@type='submit']").click()
        self.wait_for_element_with_id("id_login")
        navbar = self.browser.find_element_by_css_selector(".navbar")
        self.assertIn("Sign in", navbar.text)
        self.assertIn("Sign up", navbar.text)
        self.assertNotIn("Sign out", navbar.text)
        self.browser.find_element_by_id("id_login").click()
        username = self.browser.find_element_by_id("id_login")
        password = self.browser.find_element_by_id("id_password")
        username.send_keys("sherman")
        password.send_keys("password")
        self.browser.find_element_by_tag_name("button").click()        
        # he is redirected to his Kanji collections page
        self.fail("Implement the Kanji Card Collections page, ya bum")
