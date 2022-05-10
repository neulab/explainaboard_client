import os

from explainaboard_api_client.models import (
    PaperInfo,
    System,
    SystemCreateProps,
    SystemMetadata,
    SystemOutputProps,
)
from explainaboard_cli.tests.test_utils import test_artifacts_path, TestEndpointsE2E
from explainaboard_cli.utils import generate_dataset_id


class TestSystem(TestEndpointsE2E):
    _SYSTEM_OUTPUT = SystemOutputProps(
        data=os.path.join(test_artifacts_path, "sst2-lstm-output.txt"),
        file_type="text",
    )

    def test_no_custom_dataset(self):
        metadata = SystemMetadata(
            task="text-classification",
            is_private=True,
            model_name="test_cli",
            metric_names=["Accuracy"],
            source_language="en",
            target_language="en",
            dataset_metadata_id=generate_dataset_id("sst2", None),
            dataset_split="test",
            paper_info=PaperInfo(),  # all attributes are optional
        )
        create_props = SystemCreateProps(
            metadata=metadata, system_output=self._SYSTEM_OUTPUT
        )
        result: System = self._client.systems_post(create_props)
        try:
            sys_id = result.system_id
            sys = self._client.systems_system_id_get(sys_id)
            self.assertIn("dataset", sys)
            self.assertIn("system_info", sys)

        finally:  # cleanup
            self._client.systems_system_id_delete(sys_id)

    def test_custom_dataset(self):
        metadata = SystemMetadata(
            task="text-classification",
            is_private=True,
            model_name="test_cli",
            metric_names=["Accuracy"],
            source_language="en",
            target_language="en",
            dataset_split="test",
            paper_info=PaperInfo(),  # all attributes are optional
        )
        custom_dataset = SystemOutputProps(
            data=os.path.join(test_artifacts_path, "sst2-dataset.tsv"),
            file_type="tsv",
        )
        create_props = SystemCreateProps(
            metadata=metadata,
            system_output=self._SYSTEM_OUTPUT,
            custom_dataset=custom_dataset,
        )
        result: System = self._client.systems_post(create_props)

        # cleanup
        sys_id = result.system_id
        self._client.systems_system_id_delete(sys_id)
