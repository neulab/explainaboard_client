import os
import pathlib
from typing import Final
from unittest import TestCase

import explainaboard_client
from explainaboard_client.client import ExplainaboardClient

test_artifacts_path: Final = os.path.join(
    os.path.dirname(pathlib.Path(__file__)), "artifacts"
)


class TestEndpointsE2E(TestCase):
    def setUp(self):
        explainaboard_client.username = "explainaboard@gmail.com"
        explainaboard_client.api_key = "gEoVQz7pZzlmUR8sQiu6GQ"
        explainaboard_client.environment = "staging"
        self._client = ExplainaboardClient()

    def tearDown(self) -> None:
        self._client.close()
