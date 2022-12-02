import json
import os
import platform
from typing import Final

from explainaboard_client.tests.test_utils import TestEndpointsE2E


class TestBenchmark(TestEndpointsE2E):
    _BENCHMARK_JSON: Final = os.path.join(
        os.path.dirname(__file__), "../../example/benchmark/gaokao/config_gaokao.json"
    )
    # append the Python version to prevent DB from throwing duplicate id errors
    # in CI as tests for different Python versions are run concurrently
    _BENCHMARK_ID: Final = f"gaokao_test_cli_py{platform.python_version()}"
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
            # the "Benchmark" schema contains a "time" field
            # that is updated on every GET request
            del result["time"]
            del new_result["time"]
            self.assertDictEqual(result, new_result)

        finally:
            # cleanup
            self._client.delete_benchmark(self._BENCHMARK_ID)
