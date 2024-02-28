from fastapi.param_functions import Form
from typing_extensions import Annotated, Doc


class LoginForm:
    def __init__(
        self,
        *,
        email: Annotated[
            str,
            Form(),
            Doc(
                """
                    `email` string. The Form spec requires the exact field name
                    `email`.
                    """
            ),
        ],
        password: Annotated[
            str,
            Form(),
            Doc(
                """
                    `password` string. The OAuth2 spec requires the exact field name
                    `password".
                    """
            ),
        ],
    ):
        self.grant_type = None
        self.username = email
        self.password = password
        self.scopes = None
        self.client_id = None
        self.client_secret = None
