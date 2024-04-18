from datetime import datetime, timezone, timedelta


class UserToken:
    def __init__(self, user_email):
        self.user_email = user_email
        self._token = None

    @property
    def token(self):
        if self._token is None:
            self._token = str(hash(f"{self.user_email}{datetime.now(timezone.utc) + timedelta(minutes=60):x}"))
        return self._token