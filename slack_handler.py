import json

from tornado import gen
from tornado.web import RequestHandler
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from mindmeld_client import MindMeldClient


class SlackHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        query = "movies starring tom hanks"
        mm = MindMeldClient()
        documents = yield mm.get_documents(query)

        slack_response = "Query: {}\n".format(query)
        for i in range(len(documents)):
            slack_response += "{num}. {title}\n".format(
                num=i + 1,
                title=documents[i]["title"]
            )

        self.write(slack_response)
        self.finish()

    @gen.coroutine
    def post(self):
        # Get slack request parameters
        slack_args = self.request.arguments
        user_name = slack_args["user_name"][0].decode("utf-8")
        query = slack_args["text"][0].decode("utf-8")

        # Ask MindMeld for documents for this query
        mm = MindMeldClient()
        documents = yield mm.get_documents(query)

        #  Construct a slack message
        slack_response = "{user} asked MM \"{query}\"\n".format(
            user=user_name,
            query=query
        )
        for i in range(len(documents)):
            slack_response += "{num}. {title}\n".format(
                num=i + 1,
                title=documents[i]["title"]
            )
        yield self.post_to_slack(slack_response)
        self.finish()

    @gen.coroutine
    def post_to_slack(self, message):
        slack_body = json.dumps({
            "text": message
        })
        slack_request = HTTPRequest(
            url="https://hooks.slack.com/services/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",
            method="POST",
            body=slack_body
        )
        print("posting message to slack...")
        http_client = AsyncHTTPClient()
        yield http_client.fetch(slack_request)
        print("posted")