import requests
from bs4 import BeautifulSoup
import re

class WebCrawler(object):
	"""docstring for WebCrawler"""
	def __init__(self):
		pass

	def get_all_hyperlinks(self,seed_url,depth=2):
		""""
		This function will return all hyperlinks to crawl
		"""
		try:	
			if re.match(r'(http|https|www)://.*',seed_url):
				links_to_crawl = list()
				prepared_link = list()
				links_to_crawl.append([seed_url])
				for links in links_to_crawl:
					print "current_depth = ",depth
					if depth > 0:
						for link in links:
							prepared_link.append(link)			
							sub_links = self.get_hyperliks(link)
							if isinstance(sub_links,list):
								links_to_crawl.append(sub_links)						
					else:
						break
					depth-=1
				return prepared_link
			return "Seed Url should starts with http or https"
		except Exception as e:
			return str(e)

	def get_hyperliks(self,url):
		"""
		This function will return all hypertexted ref link current web page(url)
		"""
		sub_links = list()
		try:
			code = requests.get(url)
			plain = code.text
			s = BeautifulSoup(plain, "html.parser")
			for link in s.findAll('a'):
				hyperlinks = link.get('href')
				if hyperlinks and hyperlinks not in ["","/"]:
				# 	if re.match(r'(http|https)://.*',hyperlinks):
					if not re.match(url+r'.*',hyperlinks):
						hyperlinks = "".join([url,hyperlinks])
					sub_links.append(str(hyperlinks))
			return sub_links
		except Exception as e:
			# raise e
			return str(e)
	
	def get_images(self,links_to_crawl,seed_url=None):
		prepared_image_links_list = list()
		prepared_image_links = {}
		try:
			for link in links_to_crawl:
				image_link = self.get_image_url(link,seed_url)
				if isinstance(image_link,list):
					prepared_image_links.update({link:image_link})
			if prepared_image_links:
				prepared_image_links_list.append(prepared_image_links)
				return prepared_image_links_list
			return prepared_image_links_list
		except Exception as e:
			# raise e
			return str(e)
		
	def get_image_url(self,url,seed_url=None):
		all_images = list()
		try:
			code = requests.get(url)
			plain = code.text
			s = BeautifulSoup(plain, "html.parser")
			for image_url in s.findAll('img'):
				# img_url = str(image_url.get('data-src')) if str(image_url.get('data-src')) != None else str(image_url.get('src'))
				img_url = str(image_url.get('src'))
				if img_url == "None" or img_url in [""," "] or img_url == None:
					image_url_list = str(image_url).split()
					for attribute in image_url_list:
						match_object = re.search(r'.*[a-zA-Z0-9]-src',attribute)
						if match_object:
							img_url = str(image_url.get(match_object.group()))
				if re.match(r'(http|https)://.*',img_url):
					all_images.append(img_url)
				else:
					if ".com" in img_url:
					# if re.match(r'(.png|.com|.jpg|.jpeg)',img_url):
						img_url="https:"+img_url
						all_images.append(img_url)
					elif not re.match(url+r'.*',img_url) and seed_url:
					 	img_url = "".join([seed_url,img_url])
						all_images.append(img_url)
			return all_images
			# return [str(image_url.get('src')) for image_url in s.findAll('img') if re.match(r'(http|https)://.*',str(image_url.get('src')))]
		except Exception as e:
			# raise e
			return str(e)
	
	def get_all_links(self,seed_url,depth):
		try:
			all_hyper_links = self.get_all_hyperlinks(seed_url,depth)
			all_image_links = self.get_images(all_hyper_links,seed_url)
			return all_image_links
		except Exception as e:
			# raise e
			return str(e)