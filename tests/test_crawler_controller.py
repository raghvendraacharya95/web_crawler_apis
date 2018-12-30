import unittest
import requests
import json

class TestCrawlerController(unittest.TestCase):
	def setUp(self):
		self.base_method = "GetCrawlingUrls"
		self.base_url = "http://localhost:5000"
		self.url_delim = "/"
		self.seed_url = "https://www.travelyaari.com/"
		self.depth = ""

	def test_get_all_links_with_no_depth(self):
		method_name = "AllLinks"
		url = self.url_delim.join([self.base_url,self.base_method,method_name])
		url = url+"?seed_url="+self.seed_url+"&depth="+self.depth
		response = requests.get(url)
		print response
		expected_http_staus_code = 400
		self.assertEqual(response.status_code,expected_http_staus_code)

	def test_get_all_links_with_valid_depth(self):
		method_name = "AllLinks"
		self.depth = "1"
		url = self.url_delim.join([self.base_url,self.base_method,method_name])
		url = url+"?seed_url="+self.seed_url+"&depth="+self.depth
		response = requests.get(url)
		print response
		expected_http_staus_code = 200
		self.assertEqual(response.status_code,expected_http_staus_code)

	def test_only_get_hyper_link(self):
		pass

	def test_only_get_images_links(self):
		pass

if __name__ == '__main__':
	unittest.main()