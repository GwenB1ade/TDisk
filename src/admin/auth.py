from starlette.requests import Request
from starlette.responses import Response
from starlette_admin.auth import AdminConfig, AdminUser, AuthProvider
from starlette_admin.exceptions import FormValidationError, LoginFailed

from config import settings

ADMIN_LOGIN = settings.ADMIN_LOGIN 
ADMIN_PASS = settings.ADMIN_PASS
ADMIN_DATA = {
    "name": "Admin",
    "avatar": "admin.png",
    "company_logo_url": "admin.png",
    "roles": ["read", "create", "edit", "delete", "action_make_published"],
}


class UsernameAndPasswordProvider(AuthProvider):
    """
    This is only for demo purpose, it's not a better
    way to save and validate user credentials
    """

    async def login(
        self,
        username: str,
        password: str,
        remember_me: bool,
        request: Request,
        response: Response,
    ) -> Response:
        if len(username) < 3:
            """Form data validation"""
            raise FormValidationError(
                {"username": "Ensure username has at least 03 characters"}
            )

        if username == ADMIN_LOGIN and password == ADMIN_PASS:
            """Save `username` in session"""
            request.session.update({"username": username})
            return response

        raise LoginFailed("Invalid username or password")

    async def is_authenticated(self, request) -> bool:
        if request.session.get("username", None) == ADMIN_LOGIN:
            """
            Save current `user` object in the request state. Can be used later
            to restrict access to connected user.
            """
            request.state.user = ADMIN_DATA
            return True

        return False

    async def logout(self, request: Request, response: Response) -> Response:
        request.session.clear()
        return response