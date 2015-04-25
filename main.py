from tornado.ioloop import IOLoop
from tornado.web import RequestHandler, Application, url



class HelloHandler(RequestHandler):
	def get(self):
		print("get")
		self.write("Hello World")

	def post(self):
		print("post")
		self.write("MM response...")


def make_app():
	return Application(
		[
		url(r"/", HelloHandler)
		]
	)


def main():
	app = make_app()
	app.listen(8000)
	IOLoop.current().start()


if __name__ == "__main__":
	main()