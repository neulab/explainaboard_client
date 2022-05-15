import os
import pathlib
from typing import Final
from unittest import TestCase

from explainaboard_client.client import ExplainaboardClient
from explainaboard_client.config import Config

TEST_CONFIG = Config(
    "explainaboard@gmail.com",
    "gEoVQz7pZzlmUR8sQiu6GQ",
    "staging",
)

test_artifacts_path: Final = os.path.join(
    os.path.dirname(pathlib.Path(__file__)), "artifacts"
)


class TestEndpointsE2E(TestCase):
    def setUp(self):
        self._client = ExplainaboardClient(TEST_CONFIG)

    def tearDown(self) -> None:
        self._client.close()
