import logging
import requests
from typing import Union, TypeAlias
from tests.constants.endpoints import (LOGIN_ENDPOINT, ADMIN_EMAIL, ADMIN_PASSWORD,
                                     REGISTER_ENDPOINT, LOGOUT_ENDPOINT, REFRESH_ENDPOINT)
from tests.constants.log_messages import LogMessages
from tests.request.custom_requester import CustomRequester
from tests.models.response_models import LoginResponse, ErrorResponse
from tests.models.user_models import User

LoginApiResponse: TypeAlias = Union[LoginResponse, ErrorResponse]
RegisterApiResponse: TypeAlias = Union[User, ErrorResponse]

class AuthAPI(CustomRequester):

    def __init__(self, session: requests.Session, base_url: str) -> None:
        super().__init__(session, base_url=base_url)
        self.logger = logging.getLogger(self.__class__.__name__)

    def login(self, email: str | None = ADMIN_EMAIL, password: str | None = ADMIN_PASSWORD,
              expected_status: int = 200) -> LoginApiResponse:
        if not email or not password:
            raise ValueError("ADMIN_EMAIL и ADMIN_PASSWORD должны быть указаны в .env file")

        self.logger.info(LogMessages.Auth.ATTEMPT_LOGIN.format(email))
        payload = {"email": email, "password": password}
        response = self.post(LOGIN_ENDPOINT, data=payload, expected_status=expected_status)
        if response.ok:
            login_response = LoginResponse.model_validate(response.json())
            self.session.headers["Authorization"] = f"Bearer {login_response.access_token}"
            self.logger.info(LogMessages.Auth.LOGIN_SUCCESS.format(email))
            return login_response

        error_response = ErrorResponse.model_validate(response.json())
        self.logger.error(f"Ошибка логина для {email}: {error_response.message} (status: {error_response.statusCode})")
        return error_response

    def register(self, user_data: dict, expected_status: int = 201) -> User | ErrorResponse:
        email = user_data.get('email', 'N/A')
        self.logger.info(f"Попытка регистрации пользователя {email}")
        response = self.post(REGISTER_ENDPOINT, json=user_data, expected_status=expected_status)
        if response.ok:
            user = User.model_validate(response.json())
            self.logger.info(f"Пользователь {user.email} успешно зарегистрирован.")
            return user

        error_response = ErrorResponse.model_validate(response.json())
        self.logger.error(f"Ошибка регистрации для {email}: {error_response.message} (status: {error_response.statusCode})")
        return error_response

    def logout(self, expected_status: int = 200) -> dict | ErrorResponse:
        self.logger.info("Попытка выхода из системы (logout)")
        response = self.post(LOGOUT_ENDPOINT, expected_status=expected_status)
        if response.ok:
            self.logger.info("Выход из системы выполнен успешно")
            return response.json()
        self.logger.error(f"Ошибка выхода из системы: status {response.status_code}")
        return ErrorResponse.model_validate(response.json())

    def refresh_token(self, expected_status: int = 200) -> dict | ErrorResponse:
        self.logger.info("Попытка обновления токенов")
        response = self.post(REFRESH_ENDPOINT, expected_status=expected_status)
        if response.ok:
            self.logger.info("Токены успешно обновлены")
            return response.json()
        self.logger.error(f"Ошибка обновления токенов: status {response.status_code}")
        return ErrorResponse.model_validate(response.json())