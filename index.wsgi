import sae
from trade import wsgi

application = sae.create_wsgi_app(wsgi.application)