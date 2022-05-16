from dataclasses import dataclass
from typing import Literal, Optional

from explainaboard_api_client import Configuration


@dataclass
class Config:
    """configurations for explainaboard CLI
    :param host: if specified, it takes precedence over environment

    """

    user_email: str
    api_key: str
    environment: Literal["main", "staging", "local"] = "main"
    host: Optional[str] = None

    def __post_init__(self):
        if self.environment not in {"main", "staging", "local"}:
            raise ValueError(f"{self.environment} is not a valid environment")

    def to_client_config(self):
        client_config = Configuration()
        if self.environment == "main":
            client_config.host = "https://explainaboard.inspiredco.ai/api"
        elif self.environment == "staging":
            client_config.host = "https://dev.explainaboard.inspiredco.ai/api"
        elif self.environment == "local":
            client_config.host = "http://localhost:5000/api"

        if self.host:
            client_config.host = self.host

        client_config.username = self.user_email
        client_config.password = self.api_key
        return client_config
