from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import HTTPHeaders
from tornado import gen
import json
from urllib import parse

class MindMeldClient():
	API_URL = "https://mindmeldv2.expectlabs.com"

	METHOD_POST = "POST"
	METHOD_GET = "GET"

	def __init__(self):
		self.token = "ef0bc6f3ab1198717edad1b2c75faee01a7bc7bb"
		self.user_id = "15532"
		self.session_id = "379262"



	@gen.coroutine
	def post_text_entry(self, text):

		path = "/session/{session_id}/textentries".format(
			session_id=self.session_id
		)

		text_entry_body = {
			"text": text,
			"type": "slack",
			"weight": 1
		}
		response = yield self.call_api(MindMeldClient.METHOD_POST, path, text_entry_body)
		return response["data"]["textentryid"]


	@gen.coroutine
	def call_api(self, method_type, path, params):
		mm_auth_headers = HTTPHeaders({
			"X-MindMeld-Access-Token": "ef0bc6f3ab1198717edad1b2c75faee01a7bc7bb"
		})

		url = "{api_url}/{path}".format(
			api_url=MindMeldClient.API_URL,
			path=path
		)

		body = None
		if params is not None:
			if method_type == MindMeldClient.METHOD_GET:
				url += "?" + parse.urlencode(params)
			elif method_type == MindMeldClient.METHOD_POST:
				body = json.dumps(params)

		api_request = HTTPRequest(
			headers=mm_auth_headers,
			url=url,
			method=method_type,
			body=body
		)
		http_client = AsyncHTTPClient()
		http_response = yield http_client.fetch(api_request)
		raw_body = http_response.body.decode("utf-8")
		json_response = json.loads(raw_body)
		return json_response




	@gen.coroutine
	def get_documents(self, query):
		text_entry_id = yield self.post_text_entry(query)

		print("Text Entry ID: {}".format(text_entry_id))

		mock_documents = [
			{
				"title": "Apollo 13"
			},
			{
				"title": "Saving Private Ryan"
			}
		]
		return mock_documents


class SlackHandler(RequestHandler):

	@gen.coroutine
	def get(self):
		query = "movies starring tom hanks"
		mm = MindMeldClient()
		documents = yield mm.get_documents(query)
		self.write(json.dumps(documents))
		self.finish()

	def post(self):
		print("post")
		self.write("MM response...")


def make_app():
	return Application(
		[
			url(r"/", SlackHandler)
		]
	)


def main():
	app = make_app()
	app.listen(8000)
	IOLoop.current().start()


if __name__ == "__main__":
	main()

# one-time
# get an anon token: ef0bc6f3ab1198717edad1b2c75faee01a7bc7bb, userid: 15532
# create a session: 379262

#  on request
# post text entry to session
# get session documents
# 	*delete text entry
# write documents to response