from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


app = FastAPI(title="Online service on FastAPI")
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


from main.views import views
from main.api import api_auth
from main.api import api_cart
from main.api import api_order
from main.api import api_product
from main.api import api_user
