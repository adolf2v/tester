# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import os
from tornado.options import define, options
from handler.api import api_handlers

define("port", default=9527, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self, handlers=None):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True,
            cookie_secret="www.tester.com",
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == "__main__":
    tornado.options.options.logging = "debug"
    tornado.options.parse_command_line()
    app = Application(api_handlers)
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
