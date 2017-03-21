from user import UserHandler
from signup import SignUpHandler
from login import LoginHandler
from book import BookHandler

api_handlers = [(r'/user', UserHandler),
                (r'/signup', SignUpHandler),
                (r'/login', LoginHandler),
                (r'/book', BookHandler),
                (r'/', LoginHandler)]
