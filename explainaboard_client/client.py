from multiprocessing.pool import ApplyResult
from typing import Union

from explainaboard_api_client import ApiClient
from explainaboard_api_client.api.default_api import DefaultApi
from explainaboard_api_client.models import System, SystemCreateProps, SystemOutputProps
from explainaboard_client.config import Config
from explainaboard_client.utils import encode_file_to_base64


class ExplainaboardClient(DefaultApi):
    def __init__(self, config: Config) -> None:
        self._config = config
        api_client = ApiClient(self._config.to_client_config())
        super().__init__(api_client)

    def close(self):
        self.api_client.close()

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    def systems_post(
        self, system_create_props: SystemCreateProps, **kwargs
    ) -> Union[System, ApplyResult]:
        loaded_system_output = SystemOutputProps(
            data=encode_file_to_base64(system_create_props.system_output.data),
            file_type=system_create_props.system_output.file_type,
        )
        if "custom_dataset" in system_create_props:
            custom_dataset = SystemOutputProps(
                data=encode_file_to_base64(system_create_props.custom_dataset.data),
                file_type=system_create_props.custom_dataset.file_type,
            )
            props_with_loaded_file = SystemCreateProps(
                metadata=system_create_props.metadata,
                system_output=loaded_system_output,
                custom_dataset=custom_dataset,
            )
        else:
            props_with_loaded_file = SystemCreateProps(
                metadata=system_create_props.metadata,
                system_output=loaded_system_output,
            )
        return super().systems_post(props_with_loaded_file, **kwargs)
