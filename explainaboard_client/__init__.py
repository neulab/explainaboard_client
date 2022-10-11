from __future__ import annotations

import os
from typing import Literal

from explainaboard_client.client import ExplainaboardClient

__all__ = ["ExplainaboardClient"]

username: str | None = os.environ.get("EB_USERNAME")
api_key: str | None = os.environ.get("EB_API_KEY")
environment: Literal["main", "staging", "local"] = "main"
