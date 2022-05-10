import typing

from explainaboard_api_client import api_client, ApiClient
from explainaboard_api_client.api.default_api import DefaultApi
from explainaboard_api_client.api.default_api_endpoints.systems_post import (
    ApiResponseFor200 as SystemPostRet200,
)
from explainaboard_api_client.api.default_api_endpoints.systems_post import (
    SchemaForRequestBodyApplicationJson as SystemPostProps,
)
from explainaboard_api_client.api_client import ApiResponseWithoutDeserialization
from explainaboard_api_client.models import SystemOutputProps
from explainaboard_api_client.schemas import unset
from explainaboard_cli.config import Config
from explainaboard_cli.utils import encode_file_to_base64

# class SystemCreateLocalFile(SystemPostProps):
#     def __new__(
#         cls,
#         *args: typing.Union[dict, frozendict],
#         metadata: SystemPostProps.metadata,
#         system_output: SystemPostProps.system_output,
#         custom_dataset: typing.Union[SystemOutputProps, Unset] = unset
#     ) -> SystemCreateProps:


#         return super().__new__(
#             *args,
#             metadata=metadata,
#             system_output=system_output,
#             custom_dataset=custom_dataset
#         )


class ExplainaboardClient(DefaultApi):
    def __init__(self, config: Config) -> None:
        self._config = config
        api_client = ApiClient(self._config.to_client_config())
        super().__init__(api_client)

    def systems_post(
        self: api_client.Api,
        body: SystemPostProps,
        stream: bool = False,
        timeout: typing.Optional[typing.Union[int, typing.Tuple]] = None,
        skip_deserialization: bool = False,
    ) -> typing.Union[SystemPostRet200, ApiResponseWithoutDeserialization]:
        if isinstance(body.custom_dataset, SystemOutputProps):
            new_custom_dataset = SystemOutputProps(
                data=encode_file_to_base64(body.custom_dataset.data),
                file_type=body.custom_dataset.file_type,
            )
        else:
            new_custom_dataset = unset
        # body.system_output.data = encode_file_to_base64(body.system_output.data)
        new_system_output = SystemOutputProps(
            data=encode_file_to_base64(body.system_output.data),
            file_type=body.system_output.file_type,
        )

        return super().systems_post(
            body=SystemPostProps(
                metadata=body.metadata,
                system_output=new_system_output,
                custom_dataset=new_custom_dataset,
            ),
            stream=stream,
            timeout=timeout,
            skip_deserialization=skip_deserialization,
        )
