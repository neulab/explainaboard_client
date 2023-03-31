from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Literal, Optional


@dataclass
class HostConfig:
    host: Optional[str] = None
    frontend: Optional[str] = None


ENV_HOST_MAP: defaultdict[str, HostConfig] = defaultdict(
    HostConfig,
    {
        "main": HostConfig(
            host="https://explainaboard.inspiredco.ai",
            frontend="https://explainaboard.inspiredco.ai",
        ),
    },
)


def get_host(environment: Literal["main", "staging", "local"]):
    return ENV_HOST_MAP[environment].host


def get_frontend(environment: Literal["main", "staging", "local"]):
    return ENV_HOST_MAP[environment].frontend
