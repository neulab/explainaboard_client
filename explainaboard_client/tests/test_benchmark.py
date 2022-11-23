import json
import os
from typing import Final

from explainaboard_client.tests.test_utils import TestEndpointsE2E


class TestBenchmark(TestEndpointsE2E):
    _BENCHMARK_JSON: Final = os.path.join(
        os.path.dirname(__file__), "../../example/benchmark/gaokao/config_gaokao.json"
    )
    _BENCHMARK_ID: Final = "gaokao_test_cli"
    _BENCHMARK_NEW_NAME: Final = "gaokao_new_name"

    def test_upload_benchmark(self):
        with open(self._BENCHMARK_JSON, "r") as f:
            benchmark = json.load(f)
        # replace with our custom id for testing
        benchmark["id"] = self._BENCHMARK_ID
        try:
            self._client.upload_benchmark(benchmark)
        finally:
            # cleanup
            self._client.delete_benchmark(self._BENCHMARK_ID)

    def test_update_benchmark(self):
        with open(self._BENCHMARK_JSON, "r") as f:
            benchmark = json.load(f)
        # replace with our custom id for testing
        benchmark["id"] = self._BENCHMARK_ID
        try:
            self._client.upload_benchmark(benchmark)
            result = self._client.get_benchmark(self._BENCHMARK_ID, True)

            new_values = {"name": self._BENCHMARK_NEW_NAME}
            self._client.update_benchmark(self._BENCHMARK_ID, new_values)
            new_result = self._client.get_benchmark(self._BENCHMARK_ID, True)

            # check new value matches
            self.assertEqual(new_result["config"]["name"], self._BENCHMARK_NEW_NAME)

            # check all old values match
            del result["config"]["name"]
            del new_result["config"]["name"]
            self.assertDictEqual(result, new_result)

        finally:
            # cleanup
            self._client.delete_benchmark(self._BENCHMARK_ID)
