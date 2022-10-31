import logging
import os

from explainaboard_client.tests.test_utils import test_artifacts_path, TestEndpointsE2E


class TestSystem(TestEndpointsE2E):
    _SYSTEM_OUTPUT = os.path.join(test_artifacts_path, "sst2-lstm-output.txt")
    _DATASET = os.path.join(test_artifacts_path, "sst2-dataset.tsv")

    def test_evaluate_system_file_datalab(self):
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
            sys = self._client.get_system(sys_id)
            self.assertIn("dataset", sys)
            self.assertIn("results", sys)
        finally:  # cleanup
            self._client.delete_system(sys_id)

    def test_evaluate_system_file_custom(self):
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
        self._client.delete_system(sys_id)

    def test_evaluate_system_datalab(self):
        with open(self._SYSTEM_OUTPUT, "r") as fin:
            system_output = [{"predicted_label": x.strip()} for x in fin]
        result: dict = self._client.evaluate_system(
            system_output=system_output,
            task="text-classification",
            system_name="test_cli",
            metric_names=["Accuracy"],
            source_language="en",
            target_language="en",
            dataset="sst2",
            split="test",
            system_details={"test": "test"},
            shared_users=["explainaboard@gmail.com"],
        )
        sys_id = result["system_id"]
        try:
            sys = self._client.get_system(sys_id)
            self.assertIn("dataset", sys)
            self.assertIn("results", sys)
        finally:  # cleanup
            self._client.delete_system(sys_id)

    def test_evaluate_system_custom(self):
        with open(self._SYSTEM_OUTPUT, "r") as fin:
            system_output = [{"predicted_label": x.strip()} for x in fin]
        with open(self._DATASET, "r") as fin:
            custom_dataset = []
            for x in fin:
                text, label = x.strip().split("\t")
                custom_dataset.append({"text": text, "true_label": label})
        result: dict = self._client.evaluate_system(
            system_output=system_output,
            custom_dataset=custom_dataset,
            task="text-classification",
            system_name="test_cli",
            metric_names=["Accuracy"],
            source_language="en",
            target_language="en",
            split="test",  # TODO(gneubig): required, but probably shouldn't be
            system_details={"test": "test"},
            shared_users=["explainaboard@gmail.com"],
        )
        sys_id = result["system_id"]
        try:
            sys = self._client.get_system(sys_id)
            self.assertIn("results", sys)
        finally:  # cleanup
            self._client.delete_system(sys_id)

    def test_find_system(self):
        system_ids = []
        for i in range(2):
            result = self._client.evaluate_system_file(
                system_output_file=self._SYSTEM_OUTPUT,
                system_output_file_type="text",
                task="text-classification",
                system_name=f"test_cli{i}",
                metric_names=["Accuracy"],
                source_language="en",
                target_language="en",
                dataset="sst2",
                split="test",
                shared_users=["explainaboard@gmail.com"],
            )
            system_ids.append(result["system_id"])
        all_systems = self._client.find_systems(system_name="test_cli")
        self.assertGreater(len(all_systems), 1)
        unique_names = {x["system_name"]: 0 for x in all_systems}
        self.assertIn("test_cli0", unique_names)
        self.assertIn("test_cli1", unique_names)
        for x in system_ids:
            try:
                self._client.delete_system(x)
            except Exception:
                logging.getLogger("explainaboard_client_tests").warning(
                    f"could not delete system {x}"
                )
