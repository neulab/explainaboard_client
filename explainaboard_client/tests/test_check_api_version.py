from unittest import mock

from explainaboard_api_client.exceptions import ApiException
from explainaboard_client.tests.test_utils import TestEndpointsE2E


class TestCheckAPIVersion(TestEndpointsE2E):
    def test_check_api_version_match(self):
        info = self._client.info_get()
        self.assertEqual(info["api_version"], self._client._api_client_version)

    @mock.patch("explainaboard_client.client.input")
    def test_check_api_version_mismatch(self, mocked_input):
        # input "n" to decline auto-upgrade
        mocked_input.side_effect = ["n"]
        prev_version = self._client._api_client_version
        self._client._api_client_version = "0.0.0"
        self.assertRaises((ApiException, SystemExit), self._client.info_get)
        self._client._api_client_version = prev_version
