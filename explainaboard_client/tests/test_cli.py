from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path
import re
import tempfile
from unittest.mock import patch

import explainaboard_client
from explainaboard_client.cli import delete_systems, evaluate_system
from explainaboard_client.tests.test_utils import test_artifacts_path, TestEndpointsE2E


class TestCLI(TestEndpointsE2E):
    _SYSTEM_OUTPUT = os.path.join(test_artifacts_path, "sst2-lstm-output.txt")
    _DATASET = os.path.join(test_artifacts_path, "sst2-dataset.tsv")

    def test_evaluate_and_delete_cli(self):
        with tempfile.TemporaryDirectory() as tempdir:
            td = Path(tempdir)
            report_file = td / "report.json"
            # Evaluate system
            evaluate_args = [
                "explainaboard_client.evaluate_system",
                "--username",
                explainaboard_client.username,
                "--api-key",
                explainaboard_client.api_key,
                "--task",
                "text-classification",
                "--system-name",
                "test_cli",
                "--system-output-file",
                self._SYSTEM_OUTPUT,
                "--system-output-file-type",
                "text",
                "--dataset",
                "sst2",
                "--split",
                "test",
                "--source-language",
                "en",
                "--target-language",
                "en",
                "--report-file",
                str(report_file),
            ]
            stdout_stream = io.StringIO()
            with patch("sys.argv", evaluate_args), redirect_stdout(stdout_stream):
                evaluate_system.main()
            stdout_content = stdout_stream.getvalue()
            # print(f'---- evaluate_system stdout ----\n{stdout_content}')
            stdout_lines = stdout_content.strip().split("\n")
            m = re.match(
                r"Successfully evaluated system test_cli with ID ([0-9a-f]+)",
                stdout_lines[0],
            )
            self.assertIsNotNone(m, msg=f"evaluation failed:\n{stdout_content=}")
            sys_id = m.group(1)
            # Check that report was written properly and can be loaded
            self.assertTrue(report_file.exists(), msg="report file not found")
            json.loads(report_file.read_text())
            # Delete system
            evaluate_args = [
                "explainaboard_client.delete_systems",
                "--username",
                explainaboard_client.username,
                "--api-key",
                explainaboard_client.api_key,
                "--system-ids",
                sys_id,
                "--skip-confirmation",
            ]
            stdout_stream = io.StringIO()
            with patch("sys.argv", evaluate_args), redirect_stdout(stdout_stream):
                delete_systems.main()
            stdout_content = stdout_stream.getvalue()
            # print(f'---- delete_system stdout ----\n{stdout_content}')
            stdout_lines = stdout_content.strip().split("\n")
            self.assertEqual("Deleted 1 system", stdout_lines[-1])
