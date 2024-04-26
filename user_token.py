import uuid
from datetime import datetime, timedelta


class UserToken:
    def __init__(self, user_id):
        self.user_id = user_id
        self.access_token = self.generate_token()
        self.expire = self.calculate_expiration_token()

    def generate_token(self):
        return str(uuid.uuid4())

    def calculate_expiration_token(self):
        expiration_date = datetime.now() + timedelta(minutes=60)
        return expiration_date

    def is_valid(self):
        return datetime.now() <= self.expire

