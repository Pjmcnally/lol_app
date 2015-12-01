from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_can_enter_summoner_name_and_get_summoner_id(self):
        # A user, Bob, starts a game of League of Legends.  
        # Having heard about a new, aweseome, LoL site he navigates to it while
        # waiting to load into his game. 
        self.browser.get('http://localhost:8000')

        # Bob notices it says "Patrick's LoL App" in the title.
        self.assertIn("Patrick's LoL App", self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn("Patrick's LoL App", header_text)

        # He is invited to enter a summoner name
        inputbox = self.browser.find_element_by_id('summoner_name')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a summoner name'
        )

        # He types his summoner name into the field. 
        inputbox.send_keys('Pjmcnally')

        # When he hits enter the page displays his unique summoner ID (first step).
        inputbox.send_keys(Keys.ENTER)

        result = self.browser.find_element_by_id('name_result')
        self.assertEqual(result.text, 'Pjmcnally')

        # Bob is sutibly impressed (which is to say not very impressed).


        self.fail("Finish writing tests")

if __name__ == '__main__':
    unittest.main(warnings='ignore')
