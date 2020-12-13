from typing import List, Optional

from models.authentification.user import User


class UserAuthentification:

    def __init__(self):
        self.users: List[User] = []

    def register_user(self, login: str, password: str) -> Optional[str]:
        """Try to register user in system"""
        if self._find_user_by_login(login):
            return
        self.users.append(User(login, password))
        return login

    def login_user(self, login: str, password: str) -> Optional[str]:
        """Try to login user in system"""
        user = self._find_user_by_login(login)
        if not user:
            return
        if user.check_password(password):
            return user.login

    def _find_user_by_login(self, login: str) -> Optional[User]:
        for user in self.users:
            if user.login == login:
                return user
