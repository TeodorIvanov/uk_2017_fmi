import time
import unittest
from selenium import webdriver


class BookStoreTestCase(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)
        self.page_url = 'http://books.tto.bg/Default.aspx'
        self.login_url = 'http://books.tto.bg/Login.aspx'

    def testPageTitle(self):
        self.browser.get(self.page_url)
        self.assertIn('Book Store', self.browser.title)

    def testLogInGuest(self):
        self.browser.get(self.login_url)
        username = self.browser.find_element_by_id('Login_name')
        password = self.browser.find_element_by_id('Login_password')
        username.send_keys('guest')
        password.send_keys('guest')
        self.browser.find_element_by_id('Login_login').click()
        page_source = self.browser.page_source
        self.assertNotIn('Internal Server Error', page_source)

        self.browser.find_element_by_id('Header_Menu_Field1').click()
        time.sleep(1)
        page_source = self.browser.page_source
        self.assertIn('value="Logout"', page_source)

    def testLogInAdmin(self):
        self.browser.get(self.login_url)
        username = self.browser.find_element_by_id('Login_name')
        password = self.browser.find_element_by_id('Login_password')
        username.send_keys('admin')
        password.send_keys('admin')
        self.browser.find_element_by_id('Login_login').click()
        page_source = self.browser.page_source
        self.assertNotIn('Internal Server Error', page_source)

        self.browser.find_element_by_id('Header_Menu_Field1').click()
        time.sleep(1)
        page_source = self.browser.page_source
        self.assertIn('value="Logout"', page_source)

    def testAddItemToCart(self):
        self.testLogInAdmin()
        self.browser.get(self.page_url)
        self.browser.find_element_by_css_selector('a[href^="BookDetail"]:first-of-type').click()
        time.sleep(1)
        item_name = self.browser.find_element_by_id('Detail_name').text
        self.browser.find_element_by_id('Order_insert').click()
        time.sleep(1)
        page_source = self.browser.page_source
        self.assertIn(item_name, page_source)


if __name__ == '__main__':
    unittest.main(verbosity=2)
