import json
from urllib import parse

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import HTTPHeaders


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
        print("posting text entry: {}".format(text))
        path = "/session/{session_id}/textentries".format(
            session_id=self.session_id
        )

        text_entry_body = {
            "text": text,
            "type": "slack",
            "weight": 1
        }
        response = yield self.call_api(MindMeldClient.METHOD_POST, path, text_entry_body)
        text_entry_id = response["data"]["textentryid"]
        print("Posted, text_entry_id: {}".format(text_entry_id))
        return text_entry_id

    @gen.coroutine
    def get_session_documents(self, text_entry_id):
        print("Getting session documents for text_entry: {}".format(text_entry_id))
        path = "/session/{session_id}/documents".format(
            session_id=self.session_id
        )
        response = yield self.call_api(MindMeldClient.METHOD_GET, path)
        documents = response["data"]
        print("Received {} documents".format(len(documents)))
        return documents

    @gen.coroutine
    def call_api(self, method_type, path, params=None):
        mm_auth_headers = HTTPHeaders({
            "X-MindMeld-Access-Token": "ef0bc6f3ab1198717edad1b2c75faee01a7bc7bb"
        })

        full_url = "{api_url}/{path}".format(
            api_url=MindMeldClient.API_URL,
            path=path
        )

        body = None
        if params is not None:
            if method_type == MindMeldClient.METHOD_GET:
                full_url += "?" + parse.urlencode(params)
            elif method_type == MindMeldClient.METHOD_POST:
                body = json.dumps(params)

        api_request = HTTPRequest(
            headers=mm_auth_headers,
            url=full_url,
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
        mm_documents = yield self.get_session_documents(text_entry_id)
        return mm_documents
