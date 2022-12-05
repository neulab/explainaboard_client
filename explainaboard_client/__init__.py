from __future__ import annotations

from typing import Literal

from explainaboard_client.client import ExplainaboardClient
from explainaboard_client.data_utils import (
    wrap_tabular_dataset,
    wrap_tabular_predictions,
)

__all__ = ["ExplainaboardClient", "wrap_tabular_dataset", "wrap_tabular_predictions"]

username: str | None = None
api_key: str | None = None
environment: Literal["main", "staging", "local"] = "main"
check_api_version: bool = True
