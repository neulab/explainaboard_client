import os
import pathlib
from typing import Final
from unittest import TestCase

from explainaboard_client.client import ExplainaboardClient

test_artifacts_path: Final = os.path.join(
    os.path.dirname(pathlib.Path(__file__)), "artifacts"
)


class TestEndpointsE2E(TestCase):
    def setUp(self):
        self._client = ExplainaboardClient(
            username="explainaboard@gmail.com",
            api_key="gEoVQz7pZzlmUR8sQiu6GQ",
            environment="staging",
        )

    def tearDown(self) -> None:
        self._client.close()
