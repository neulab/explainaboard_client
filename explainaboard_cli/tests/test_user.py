from unittest import TestCase

from explainaboard_api_client import ApiException
from explainaboard_cli.client import ExplainaboardClient
from explainaboard_cli.config import Config
from explainaboard_cli.tests.test_utils import TEST_CONFIG


class TestUserAPI(TestCase):
    def setUp(self):
        self._client = ExplainaboardClient(TEST_CONFIG)

    def tearDown(self) -> None:
        self._client.close()

    def test_can_fetch_user_info(self):
        user = self._client.user_get()
        self.assertEqual(user.body.email, "explainaboard@gmail.com")

    def test_401(self):
        client = ExplainaboardClient(
            Config("invalid_username", "invalid_api_key", "staging")
        )
        with self.assertRaises(ApiException):
            client.user_get()
