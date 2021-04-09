from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
class MySeleniumTests(LiveServerTestCase):
    # class logic below
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver('./chromedriver')

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
