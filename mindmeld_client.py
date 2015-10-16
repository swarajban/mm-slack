import json
from urllib import parse

from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest
from tornado.httputil import HTTPHeaders


class MindMeldClient():
    """
    A MindMeld Client for Tornado web server
    """

    API_URL = "https://api-west-dev-e.expectlabs.com"

    METHOD_POST = "POST"
    METHOD_GET = "GET"

    def __init__(self):
        self.token = "13c712a4d9476f54549a62f66972025116cdb433"
        self.user_id = "1514"
        self.session_id = "567873"

    # Get documents for a query by submitting a text entry
    # and getting session documents
    @gen.coroutine
    def get_documents(self, query):
        text_entry_id = yield self.post_text_entry(query)
        mm_documents = yield self.get_session_documents(text_entry_id)
        return mm_documents

    # Post a text entry to the MM API & return the text entry id
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

    # Given a text entry id, get session documents for the text entry
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

    # High-level wrapper for MM API. Accepts a method type path, and params
    # Automatically handles setting token in header, encoding params &
    # json decoding response
    @gen.coroutine
    def call_api(self, method_type, path, params=None):
        mm_auth_headers = HTTPHeaders({
            "X-MindMeld-Access-Token": self.token
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


