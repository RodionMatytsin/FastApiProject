from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


main = FastAPI(title="Online service on FastAPI")


from main.api import api_auth
from main.api import api_cart
from main.api import api_order
from main.api import api_product
from main.api import api_user
