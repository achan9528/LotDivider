from django.contrib.staticfiles.testing import LiveServerTestCase
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.keys import Keys
class MySeleniumTests(LiveServerTestCase):
    # class logic below
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = WebDriver('./chromedriver')

    def test_collapseTable(self):
        driver = self.selenium
        driver.get("http://localhost:8000/")
        email = driver.find_element_by_name("email")
        pw = driver.find_element_by_name("password")
        button = driver.find_elements_by_tag_name("button")
        

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()
