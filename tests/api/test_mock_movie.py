import allure
from datetime import datetime
import pytest_check as check
import pytest
import logging

from tests.clients.api_manager import ApiManager
from tests.constants.endpoints import NON_EXISTENT_ID
from tests.models.movie_models import Movie, Genre
from tests.models.response_models import ErrorResponse
from tests.models.request_models import MovieCreate
from tests.utils.decorators import allure_test_details

LOGGER = logging.getLogger(__name__)

@allure.epic("Мок тесты")
@allure.feature("Тесты с использованием моков")
class TestMockingExamples:

    @allure_test_details(
        story="Использование мока для изоляции сервисов",
        title="Тест удаления несуществующего фильма, полученного из мока",
        description="""
        Этот тест демонстрирует использование мока для симуляции ответа от сервиса.
        Шаги:
        1. Мокируется метод `create_movie` для возврата заранее определенного объекта фильма.
        2. Вызывается метод `create_movie` - он возвращает мок-объект без реального запроса к API.
        3. Вызывается метод `delete_movie` с ID из мок-объекта.
        4. Проверяется, что API удаления возвращает ошибку 404, так как фильма с таким ID на самом деле не существует.
        """,
        severity=allure.severity_level.NORMAL,
    )
    def test_delete_movie_from_mocked_creation(self, admin_api_manager: ApiManager, movie_payload: MovieCreate, mocker):
        LOGGER.info("Запуск теста: test_delete_movie_from_mocked_creation")
        with allure.step("1. Подготовка данных для мока на основе фикстуры 'movie_payload'"):
            fake_movie_id = NON_EXISTENT_ID
            fake_movie = Movie(
                id=fake_movie_id,
                name=movie_payload.name,
                description=movie_payload.description,
                price=movie_payload.price,
                location=movie_payload.location,
                published=movie_payload.published,
                genreId=movie_payload.genre_id,
                imageUrl=None,
                genre=Genre(name="Жанр из мока"),
                createdAt=datetime.now(),
                rating=0.0
            )
            LOGGER.info(f"Подготовлен мок-объект для фильма с ID {fake_movie_id}")

        with allure.step("2. Мокирование метода 'create_movie'"):
            LOGGER.info("Мокируем метод 'create_movie', чтобы он возвращал наш фейковый объект")
            mocker.patch.object(
                admin_api_manager.movies_api,
                'create_movie',
                return_value=fake_movie
            )

        with allure.step("3. 'Создание' фильма (на самом деле вызов мока с данными из фикстуры)"):
            LOGGER.info("Вызываем create_movie, который теперь является моком")
            created_movie_from_mock = admin_api_manager.movies_api.create_movie(movie_data=movie_payload)

            is_movie = isinstance(created_movie_from_mock, Movie)
            check.is_true(is_movie, f"Мок должен был вернуть объект Movie, а не {type(created_movie_from_mock)}")
            if is_movie:
                check.equal(created_movie_from_mock.id, fake_movie_id)
                check.equal(created_movie_from_mock.name, movie_payload.name)
                LOGGER.info("Мок-объект фильма успешно 'создан' и проверен")

                with allure.step("4. Попытка удалить реально несуществующий фильм по ID из мока"):
                    LOGGER.info(f"Попытка удалить реальный фильм с ID из мока: {created_movie_from_mock.id}")
                    delete_response = admin_api_manager.movies_api.delete_movie(
                        movie_id=created_movie_from_mock.id,
                        expected_status=404
                    )

                with allure.step("5. Проверка, что API вернуло ошибку 404 Not Found"):
                    is_error = isinstance(delete_response, ErrorResponse)
                    check.is_true(is_error, f"Ожидался объект ErrorResponse, но получен {type(delete_response)}")
                    if is_error:
                        LOGGER.info(f"Получена ожидаемая ошибка 404: {delete_response.message}")
                        check.equal(delete_response.statusCode, 404)
                        check.equal(delete_response.message, "Фильм не найден")
            else:
                LOGGER.error(f"Мок вернул некорректный тип ({type(created_movie_from_mock)}), тест прерван.")
                pytest.fail("Мок вернул некорректный тип, дальнейшая проверка невозможна.") 