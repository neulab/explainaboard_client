from multiprocessing.pool import ApplyResult

from explainaboard_api_client import ApiException
import explainaboard_client
from explainaboard_client.client import ExplainaboardClient
from explainaboard_client.tests.test_utils import TestEndpointsE2E


class TestUserAPI(TestEndpointsE2E):
    def test_can_fetch_user_info(self):
        user = self._client.user_get()
        self.assertEqual(user["email"], "explainaboard@gmail.com")

    def test_401(self):
        explainaboard_client.username = "invalid_username"
        explainaboard_client.api_key = "invalid_api_key"
        explainaboard_client.environment = "staging"
        client = ExplainaboardClient()
        with self.assertRaises(ApiException):
            client.user_get()

    def test_async(self):
        thread: ApplyResult = self._client.user_get(async_req=True)
        user = thread.get()
        self.assertEqual(user["email"], "explainaboard@gmail.com")
