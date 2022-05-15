from multiprocessing.pool import ApplyResult

from explainaboard_api_client import ApiException
from explainaboard_client.client import ExplainaboardClient
from explainaboard_client.config import Config
from explainaboard_client.tests.test_utils import TestEndpointsE2E


class TestUserAPI(TestEndpointsE2E):
    def test_can_fetch_user_info(self):
        user = self._client.user_get()
        self.assertEqual(user["email"], "explainaboard@gmail.com")

    def test_401(self):
        client = ExplainaboardClient(
            Config("invalid_username", "invalid_api_key", "staging")
        )
        with self.assertRaises(ApiException):
            client.user_get()

    def test_async(self):
        thread: ApplyResult = self._client.user_get(async_req=True)
        user = thread.get()
        self.assertEqual(user["email"], "explainaboard@gmail.com")
