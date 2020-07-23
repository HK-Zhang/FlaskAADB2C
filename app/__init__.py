from flask import Flask,url_for
from flask_session import Session  # https://pythonhosted.org/Flask-Session
from config import appinsightKey,apiversion,load_config
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler
import logging
from flasgger import Swagger,swag_from
from os import listdir
from os.path import isfile, join
import socket
import app_config_b2c
# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/1.0.x/deploying/wsgi-standalone/#proxy-setups
from werkzeug.middleware.proxy_fix import ProxyFix

hostname=socket.gethostname()
format_str = f'{apiversion}@{hostname} says:'+'%(asctime)s - %(levelname)-8s - %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
logging.basicConfig(level=logging.INFO)
formatter = logging.Formatter(format_str, date_format)
rootlogger = logging.getLogger()

app = Flask(__name__)
app.config.from_object(app_config_b2c)
Session(app)
handler = AzureLogHandler(connection_string=f'InstrumentationKey={appinsightKey}')
handler.setFormatter(formatter)
rootlogger.addHandler(handler)
middleware = FlaskMiddleware(app,exporter=AzureExporter(connection_string=f'InstrumentationKey={appinsightKey}'),sampler=ProbabilitySampler(rate=1.0))    

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

load_config()

Swagger(app)    
from app.api import api as api_blueprint
app.register_blueprint(api_blueprint, url_prefix='/v1')
from app.web import web as web_blueprint
app.register_blueprint(web_blueprint)
from app.web.views import _build_auth_url
app.jinja_env.globals.update(
    _build_auth_url=_build_auth_url)  # Used in template

logging.info(f'App Started {apiversion}.')

