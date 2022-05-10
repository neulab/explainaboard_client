import os
import pathlib
from typing import Final

from explainaboard_cli.config import Config

TEST_CONFIG = Config(
    "explainaboard@gmail.com",
    "gEoVQz7pZzlmUR8sQiu6GQ",
    "local",
)

test_artifacts_path: Final = os.path.join(
    os.path.dirname(pathlib.Path(__file__)), "artifacts"
)
