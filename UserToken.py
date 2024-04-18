from datetime import datetime, timezone, timedelta


class UserToken:
    def __init__(self, user_id):
        self.user_id = user_id
        self._token = None

    @property
    def token(self):
        if self._token is None:
            self._token = str(hash(f"{self.user_id}{datetime.now(timezone.utc) + timedelta(minutes=60):x}"))
        return self._token