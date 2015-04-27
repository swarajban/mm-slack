from tornado.ioloop import IOLoop
from tornado.web import Application, url
from slack_handler import SlackHandler

import os


# Creates Tornado Application w/ Routes
def make_app():
    return Application(
        [
            url(r"/", SlackHandler)
        ]
    )


# Initializes Tornado server
def main():
    app = make_app()
    port = int(os.environ.get("PORT", 8000))
    app.listen(port)
    IOLoop.current().start()


if __name__ == "__main__":
    main()
