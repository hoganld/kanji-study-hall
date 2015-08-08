from django.test import LiveServerTestCase

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class FunctionalTest(LiveServerTestCase):
    """This class serves as a simple base class for the other functional test
    classes, where the action happens.

    """

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(5)
    
    def tearDown(self):
        self.browser.quit()
        super().tearDown()

    def wait_for_element_with_id(self, element_id):
        WebDriverWait(self.browser, timeout=30).until(
            lambda b: b.find_element_by_id(element_id),
            'Could not find element with id {}. Page text was:\n()'.format(
                element_id, self.browser.find_element_by_tag_name('body').text
            )
        )

