from vercel_python_wsgi import vercel_wsgi
from app import app as flask_app


app = vercel_wsgi(flask_app)