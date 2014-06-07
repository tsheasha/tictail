import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class TodoAutoTest(unittest.TestCase):

    def setUp(self):
        """
        Set up Driver to Firefox and submit login form
        """
        self.driver = webdriver.Firefox()
        self.driver.get("http://127.0.0.1:5000/")
        self.assertIn("TicTail Todo", self.driver.title)
        elem = self.driver.find_element_by_name("username")
        elem.send_keys("tsheasha")
        elem = self.driver.find_element_by_name("password")
        elem.send_keys("password")
        elem = self.driver.find_element_by_name("login").click()



    def test_login(self):
        """
        Test that login succeeds
        """
        driver = self.driver
        assert driver.find_element_by_link_text("Logout") != None

    def test_create(self):
        """
        Test that a logged in user can add a new todo
        """
        driver = self.driver
        elem = self.driver.find_element_by_id("new-todo")
        elem.send_keys("Auto test")
        elem.send_keys(Keys.RETURN)
        
        elem = self.driver.find_element_by_id("new-todo")
        elem.send_keys("Auto test as well")
        elem.send_keys(Keys.RETURN)

        assert "Auto test" in driver.page_source
        assert "Auto test as well" in driver.page_source

    def tearDown(self):
        self.driver.close()

if __name__ == "__main__":
    unittest.main()
