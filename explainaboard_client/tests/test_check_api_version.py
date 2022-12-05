from collections.abc import Callable
from contextlib import redirect_stdout
import io
from unittest.mock import patch

from explainaboard_api_client.exceptions import ApiException
import explainaboard_client
from explainaboard_client.cli import delete_systems
from explainaboard_client.client import ExplainaboardClient
from explainaboard_client.exceptions import APIVersionMismatchException
from explainaboard_client.tests.test_utils import TestEndpointsE2E


def _with_wrong_api_version(func: Callable) -> Callable:
    def wrapper(self, *args, **kwargs):
        prev_version = self._client._api_client_version
        self._client._api_client_version = "0.0.0"
        result = func(self, *args, **kwargs)
        self._client._api_client_version = prev_version
        return result

    return wrapper


class TestCheckAPIVersion(TestEndpointsE2E):
    def test_check_api_version_match(self):
        info = self._client.info_get()
        self.assertEqual(info["api_version"], self._client._api_client_version)

    @_with_wrong_api_version
    def test_check_api_version_mismatch(self):
        self.assertRaises(
            (ApiException, APIVersionMismatchException),
            self._client.info_get,
        )

    @_with_wrong_api_version
    @patch("explainaboard_client.client_utils.input")
    def test_check_api_version_mismatch_cli(self, mocked_input):
        # input "n" to decline auto-upgrade
        mocked_input.side_effect = ["n"]
        with patch(
            "explainaboard_client.cli.delete_systems.ExplainaboardClient"
        ) as PatchedClient:
            # patch with our client, which has the wrong api version
            PatchedClient.return_value = self._client
            evaluate_args = [
                "explainaboard_client.delete_systems",
                "--username",
                explainaboard_client.username,
                "--api-key",
                explainaboard_client.api_key,
                "--system-ids",
                "a-fake-id",
                "--skip-confirmation",
            ]
            stdout_stream = io.StringIO()
            with patch("sys.argv", evaluate_args), redirect_stdout(stdout_stream):
                with self.assertRaises(
                    (ApiException, APIVersionMismatchException, SystemExit)
                ):
                    delete_systems.main()


class TestCheckAPIVersionDisabled(TestEndpointsE2E):
    def setUp(self):
        super().setUp()
        # disable API version checking
        explainaboard_client.check_api_version = False
        self._client = ExplainaboardClient()

    @_with_wrong_api_version
    def test_check_api_version_disabled(self):
        # should execute with no exception raised
        _ = self._client.info_get()
