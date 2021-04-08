#for all selenium

import unittest
from selenium import webdriver

class InputTest(unittest.TestCase):
    def setUp(self):
        #setup the test by opening browser
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.get("file:///C:/Users/vissh/source/repos/VisshaalS/Capstone-Project/RecommendMan/Steve_index.html")
        
    def test_inputs(self):
        #get the text input
        self.text_input = self.driver.find_element_by_id("chat-input")

        #enter the search and submit
        self.text_input.send_keys("testing")
        self.text_input.submit()

        #see what the output is
        list = self.driver.find_element_by_class_name("message-box")
        self.assertEquals("Sorry, I didn't get that. Can you rephrase it?",list)
    
    def tearDown(self):
        #close down the browser
        self.driver.quit()

