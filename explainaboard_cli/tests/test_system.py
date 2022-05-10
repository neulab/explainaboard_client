import os
from unittest import TestCase

from explainaboard_api_client.models import (
    PaperInfo,
    SystemCreateProps,
    SystemMetadata,
    SystemOutputProps,
)
from explainaboard_cli.client import ExplainaboardClient
from explainaboard_cli.tests.test_utils import test_artifacts_path, TEST_CONFIG
from explainaboard_cli.utils import generate_dataset_id


class TestSystem(TestCase):
    def setUp(self):
        self._client = ExplainaboardClient(TEST_CONFIG)

    def tearDown(self) -> None:
        self._client.close()

    def test_no_custom_dataset(self):
        metadata = SystemMetadata(
            task="text-classification",
            is_private=True,
            model_name="test_cli",
            metric_names=["Accuracy"],
            dataset_metadata_id=generate_dataset_id("sst2", None),
            dataset_split="test",
            paper_info=PaperInfo({}),  # all attributes are optional
        )
        system_output = SystemOutputProps(
            data=os.path.join(test_artifacts_path, "sst2-lstm-output.txt"),
            file_type="text",
        )
        create_props = SystemCreateProps(metadata=metadata, system_output=system_output)
        result = self._client.systems_post(create_props)
        print(result)

    def test_get(self):
        sys = self._client.systems_system_id_get(
            {"system_id": "627967e746792d474a761e71"}
        )
        print(sys.body.dataset)
        print(sys.body.creator)
