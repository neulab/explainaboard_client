from __future__ import annotations

from typing import Literal

from explainaboard_client.client import ExplainaboardClient

__all__ = ["ExplainaboardClient"]

username: str | None = None
api_key: str | None = None
environment: Literal["main", "staging", "local"] = "main"
