import os

DATABASE_USER = 'postgres' if os.getenv('DATABASE_USER') is None else os.getenv('DATABASE_USER')
DATABASE_PASSWORD = 'root' if os.getenv('DATABASE_PASSWORD') is None else os.getenv('DATABASE_PASSWORD')
DATABASE_IP = 'localhost' if os.getenv('DATABASE_IP') is None else os.getenv('DATABASE_IP')
DATABASE_PORT = 5454 if os.getenv('DATABASE_PORT') is None else os.getenv('DATABASE_PORT')
DATABASE_NAME = 'FastAPI' if os.getenv('DATABASE_NAME') is None else os.getenv('DATABASE_NAME')
