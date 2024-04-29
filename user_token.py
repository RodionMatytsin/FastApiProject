from uuid import uuid4
from datetime import datetime, timedelta


class UserToken:
    def __init__(self, user_id):
        self.user_id = user_id
        self.access_token = self.generate_token()
        self.expire = self.calculate_expiration_token()
        self.datetime_create = self.datetime_of_creation()

    def generate_token(self):
        return str(uuid4())

    def calculate_expiration_token(self):
        expiration_date = datetime.now() + timedelta(weeks=1)
        return expiration_date

    def datetime_of_creation(self):
        return datetime.now()

    def is_valid(self):
        return datetime.now() <= self.expire
