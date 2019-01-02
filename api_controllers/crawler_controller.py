from flask_restplus import Namespace, Resource, fields
from flask_restplus import reqparse
from flask import Flask
from web_crawler.crawler import WebCrawler

api = Namespace('GetCrawlingUrls', description='Get Crawling Urls')
application = Flask(__name__)

BaseResponse = {
	"data" : [],"ErrMsg" : None, "StatusCode": 1, "Success":True
}

all_links_parser = reqparse.RequestParser()
all_links_parser.add_argument('seed_url', type=str)
all_links_parser.add_argument('depth', type=str)

image_links_parser = reqparse.RequestParser()
image_links_parser.add_argument('url',type=str)


@application.before_request
def initialize_base_response():
	BaseResponse = {"data" : [],"ErrMsg" : None, "StatusCode": 1, "Success":True}

@api.route('/AllLinks')
class GetAllLinks(Resource):
	@api.expect(all_links_parser)
	@api.doc(security='apikey',params={'seed_url': 'Seed Url to crawl','depth':'Depth of seed url.'})
	def get(self):
		
		"""
		This API will return all hypertexted ref links in requested url with given depth along with all images links
		"""
		##Note - Can Use dictionary as switcher to api - ToDo
		BaseResponse = {"data" : [],"ErrMsg" : None, "StatusCode": 1, "Success":True}
		request = all_links_parser.parse_args()
		is_success = True
		if request["depth"]:
			seed_url = request["seed_url"]
			depth = int(request["depth"])
			crawler = WebCrawler()
			all_links = crawler.get_all_links(seed_url,depth)
			if isinstance(all_links,list):
				if len(all_links) > 0:
					BaseResponse["data"] = all_links
				else:
					is_success = False
			else:
				is_success = False
			if is_success == False:
				BaseResponse["ErrMsg"] = "Unable to fetch"
				BaseResponse["StatusCode"] = "-1"
				BaseResponse["Success"] = False
			return BaseResponse, 200
		else:
			BaseResponse["ErrMsg"] = "PLease pass depth"
			BaseResponse["StatusCode"] = "-1"
			BaseResponse["Success"] = False
		return BaseResponse,400


@api.route('/ImagesLinks')
class GetImagesLinks(Resource):
	@api.expect(image_links_parser)
	@api.doc(security='apikey',params={'url': 'Url to get all images links'})
	def get(self):
		# BaseResponse = {"data" : [],"ErrMsg" : None, "StatusCode": 1}
		"""
		This API Will return all images links in requested url
		"""
		BaseResponse = {"data" : [],"ErrMsg" : None, "StatusCode": 1, "Success":True}
		request = image_links_parser.parse_args()
		url = request["url"]
		crawler = WebCrawler()
		all_images_link = crawler.get_image_url(url)
		if isinstance(all_images_link,list):
			BaseResponse["data"] = all_images_link
		else:
			# error_msg = all_images_link
			# BaseResponse["ErrMsg"] = all_images_link
			BaseResponse["ErrMsg"] = "Unable to fetch ImagesLinks("+all_images_link+")"
			BaseResponse["StatusCode"] = "-1"
			BaseResponse["Success"] = False
		return BaseResponse, 200

@api.route('/AllPages')
class GetAllPages(Resource):
	@api.expect(all_links_parser)
	@api.doc(security='apikey',params={'seed_url': 'Seed Url to crawl','depth':'Depth of seed url.'})
	def get(self):
		"""
		This API will return only hypertexted ref links in requested url(web page) with given depth
		"""
		BaseResponse = {"data" : [],"ErrMsg" : None, "StatusCode": 1, "Success":True}
		request = all_links_parser.parse_args()
		if request["depth"]:
			seed_url = request["seed_url"]
			depth = int(request["depth"])
			crawler = WebCrawler()
			all_hyper_links = crawler.get_all_hyperlinks(seed_url,depth)
			if isinstance(all_hyper_links,list):
				BaseResponse["data"] = all_hyper_links
			else:
				# BaseResponse["ErrMsg"] = all_hyper_links
				BaseResponse["ErrMsg"] = "Unable to fetch"+str(all_hyper_links)
				BaseResponse["StatusCode"] = "-1"
				BaseResponse["Success"] = False
			return BaseResponse, 200
		else:
			BaseResponse["ErrMsg"] = "PLease pass depth"
			BaseResponse["StatusCode"] = "-1"
			BaseResponse["Success"] = False
		return BaseResponse,400
