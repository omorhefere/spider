import unittest
from scraper import crawl_page, crawler_bfs, get_static_links
import sys

class crawler_tests(unittest.TestCase):
    def setUp(self):
        self.first_url = 'http://www.techcrunch.com/'
        self.url_set = set([self.first_url])


    def test_output(self):
        #check the tyoe of the outputs
        page = crawl_page(self.url_set,self.first_url)
        page_set = crawler_bfs(self.first_url, 1)
        static = get_static_links(self.first_url)

        self.assertIsInstance(page, set)
        self.assertIsInstance(page_set, set)
        self.assertIsInstance(static, dict)
    def test_starting_url_different(self):
        #check that starting url doesn't change inside function
        self.assertItemsEqual(self.url_set, crawler_bfs(self.first_url, 0))
    def test_valide_input_url(self):
        #check that function raises an erro when you input invalid urls
        url = 'http://ooimoloame.co.uk/'
        error = 'Invalid url, please input a valid url'
        with self.assertRaises(Exception) as context:
            crawler_bfs(url, 0)

        self.assertTrue(error in context.exception)



if __name__ == '__main__':
    unittest.main()
