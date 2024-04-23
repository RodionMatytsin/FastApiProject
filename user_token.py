from datetime import datetime, timezone, timedelta


class UserToken:
    def __init__(self, username):
        self.username = username
        self._token = None

    @property
    def token(self):
        if self._token is None:
            self._token = str(hash(f"{self.username}{datetime.now(timezone.utc) + timedelta(minutes=60)}"))
        return self._token