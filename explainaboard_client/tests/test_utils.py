import os
import pathlib
from typing import Final
from unittest import TestCase

import explainaboard_client
from explainaboard_client.client import ExplainaboardClient
from explainaboard_api_client.exceptions import NotFoundException

test_artifacts_path: Final = os.path.join(
    os.path.dirname(pathlib.Path(__file__)), "artifacts"
)


class TestEndpointsE2E(TestCase):
    def setUp(self) -> None:
        explainaboard_client.username = "explainaboard@gmail.com"
        explainaboard_client.api_key = "gEoVQz7pZzlmUR8sQiu6GQ"
        explainaboard_client.environment = "staging"
        self._client = ExplainaboardClient()

    def tearDown(self) -> None:
        self._client.close()

class TestEndpointsE2EWithSystemDeletion(TestEndpointsE2E):
    def setUp(self) -> None:
        super().setUp()
        self._system_ids_to_delete = []

    def tearDown(self) -> None:
        for sys_id in self._system_ids_to_delete:
            try:
                self._client.delete_system(sys_id)
            # ingore 404 exceptions as it means
            # the system has been deleted successfully
            except NotFoundException:
                pass
        super().tearDown()
