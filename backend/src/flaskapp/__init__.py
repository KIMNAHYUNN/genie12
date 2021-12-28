from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# for security
class SecureFlask(Flask):
    def process_response(self, response):
        # Every response will be processed here first
        response.headers['server'] = 'GENIE'
        super(SecureFlask, self).process_response(response)

        return response

app = Flask(__name__)

app.wsgi_app = ProxyFix(app.wsgi_app)
from flaskapp import views