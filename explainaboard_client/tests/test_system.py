import os

from explainaboard_client.tests.test_utils import test_artifacts_path, TestEndpointsE2E


class TestSystem(TestEndpointsE2E):
    _SYSTEM_OUTPUT = os.path.join(test_artifacts_path, "sst2-lstm-output.txt")
    _DATASET = os.path.join(test_artifacts_path, "sst2-dataset.tsv")

    def test_no_custom_dataset(self):
        result: dict = self._client.evaluate_system_file(
            system_output_file=self._SYSTEM_OUTPUT,
            system_output_file_type="text",
            task="text-classification",
            system_name="test_cli",
            metric_names=["Accuracy"],
            source_language="en",
            target_language="en",
            dataset="sst2",
            split="test",
            shared_users=["explainaboard@gmail.com"],
        )
        sys_id = result["system_id"]
        try:
            sys = self._client.systems_get_by_id(sys_id)
            self.assertIn("dataset", sys)
            self.assertIn("system_info", sys)
        finally:  # cleanup
            self._client.systems_delete_by_id(sys_id)

    def test_custom_dataset(self):
        result: dict = self._client.evaluate_system_file(
            system_output_file=self._SYSTEM_OUTPUT,
            system_output_file_type="text",
            custom_dataset_file=self._DATASET,
            custom_dataset_file_type="tsv",
            task="text-classification",
            system_name="test_cli",
            metric_names=["Accuracy"],
            source_language="en",
            target_language="en",
            split="test",  # TODO(gneubig): required, but probably shouldn't be
            shared_users=["explainaboard@gmail.com"],
        )
        # cleanup
        sys_id = result["system_id"]
        self._client.systems_delete_by_id(sys_id)
