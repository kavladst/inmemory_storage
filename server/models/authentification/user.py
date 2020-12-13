import bcrypt


class User:

    def __init__(self, login: str, password: str):
        self.login = login
        self._hashed_password = bcrypt.hashpw(
            password.encode('utf-8'), bcrypt.gensalt()
        )

    def check_password(self, password: str) -> bool:
        """Check password for user"""
        return bcrypt.checkpw(password.encode('utf-8'), self._hashed_password)
