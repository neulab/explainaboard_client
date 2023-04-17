from __future__ import annotations

from collections.abc import Callable
import json
import logging
from multiprocessing.pool import ApplyResult
import re
from typing import Any, Literal, Union

from explainaboard_api_client import __name__ as api_client_name
from explainaboard_api_client import __version__ as api_client_version
from explainaboard_api_client import ApiClient, Configuration
from explainaboard_api_client.api.default_api import DefaultApi
from explainaboard_api_client.api_client import Endpoint
from explainaboard_api_client.exceptions import ApiException
from explainaboard_api_client.model.system_metadata import SystemMetadata
from explainaboard_api_client.model.systems_return import SystemsReturn
from explainaboard_api_client.models import (
    Benchmark,
    BenchmarkConfig,
    BenchmarkCreateProps,
    BenchmarkDatasetConfig,
    BenchmarkMetric,
    BenchmarkOperationConfig,
    BenchmarkUpdateProps,
    BenchmarkViewConfig,
    Paper,
    System,
    SystemCreateProps,
    SystemOutputProps,
)
import explainaboard_client
from explainaboard_client.client_utils import (
    encode_file_to_base64,
    encode_string_to_base64,
)
from explainaboard_client.config import get_host
from explainaboard_client.exceptions import APIVersionMismatchException
from explainaboard_client.tasks import DEFAULT_METRICS, infer_file_type, TaskType


class ExplainaboardClient:
    # ---- Initializers, etc.
    def __init__(self) -> None:
        """Initialize the ExplainaBoard client."""
        host = get_host(explainaboard_client.environment)
        api_client = ApiClient(
            Configuration(
                username=explainaboard_client.username,
                password=explainaboard_client.api_key,
                host=host,
            )
        )
        self._default_api: DefaultApi = DefaultApi(api_client)
        self._active: bool = True

        self._api_version_param = "x_api_version"
        self._api_version_header = "X-API-version"
        self._api_client_version = api_client_version

        def with_check_api_version(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                try:
                    return func(*args, **kwargs, x_api_version=self._api_client_version)
                except ApiException as e:
                    body = json.loads(e.body)
                    if body["error_code"] == 40001:
                        detail = body["detail"]
                        package = api_client_name.replace("_", "-")
                        match = re.search("(\\d+\\.\\d+.\\d+)", detail)
                        if match:
                            required_version = detail[match.start() : match.end()]
                            message = (
                                f"{detail} "
                                + "Installation command: "
                                + f"pip install {package}=={required_version}"
                            )
                            raise APIVersionMismatchException(
                                message,
                                package,
                                required_version,
                                self._api_client_version,
                            ) from e
                        else:
                            raise RuntimeError(
                                "Unable to parse required API version from message: "
                                f"{detail}. Please contact admin."
                            ) from e
                    else:
                        raise e

            return wrapper

        if explainaboard_client.check_api_version:
            # The code below does two things:
            # 1. modifies the api client's validation rule of every endpoint
            # to allow us to specify the X-API-version header in every request
            # without having to define it in openapi.yaml
            # 2. decorates the call_with_http_info of every endpoint
            # so the api version header is attached in every request.
            for v in vars(self._default_api).values():
                if type(v) == Endpoint:
                    v.params_map["all"].append(self._api_version_param)
                    v.openapi_types[self._api_version_param] = (str,)
                    v.attribute_map[self._api_version_param] = self._api_version_header
                    v.location_map[self._api_version_param] = "header"

                    v.call_with_http_info = with_check_api_version(
                        v.call_with_http_info
                    )

    def close(self):
        self._default_api.api_client.close()
        self._active = False

    def __enter__(self):
        return self

    def __exit__(self):
        self.close()

    # ---- Client Functions
    def evaluate_system(
        self,
        task: str,
        system_name: str,
        system_output: list[dict],
        dataset: str | None = None,
        sub_dataset: str | None = None,
        split: str | None = None,
        custom_dataset: list[dict] | dict[str, Any] | None = None,
        metric_names: list[str] | None = None,
        source_language: str | None = None,
        target_language: str | None = None,
        system_details: dict | None = None,
        public: bool = False,
        shared_users: list[str] | None = None,
        system_tags: list[str] | None = None,
    ) -> dict:
        """Evaluate a system output file and return a dictionary of results.

        Args:
            task: What task you will be analyzing.
            system_name: Name of the system that you are evaluating.
            system_output: Examples in the system output.
            dataset: A dataset name from DataLab.
            sub_dataset: A sub-dataset name from DataLab.
            split: The name of the dataset split to process.
            custom_dataset: Examples in the custom dataset.
            metric_names: The metrics to compute, leave blank for task defaults
            source_language: The language on the input side.
            target_language: The language on the output side.
            system_details: File of system details in JSON format.
            public: Make the evaluation results public.
            shared_users: Emails of users to share with.
            system_tags: User defined tags for the system,
                useful for searching and grouping systems
        """
        # Sanity checks
        if not (source_language or target_language):
            raise ValueError("You must specify source and/or target language")
        if custom_dataset:
            custom_dataset_examples = (
                custom_dataset
                if isinstance(custom_dataset, list)
                else custom_dataset["examples"]
            )
            if len(custom_dataset_examples) != len(system_output):
                raise ValueError(
                    "Custom dataset must have the same length as system output"
                )

        # Infer missing values
        task = TaskType(task)
        metric_names = metric_names or DEFAULT_METRICS[task]
        source_language = source_language or target_language
        target_language = target_language or source_language
        shared_users = shared_users or []
        system_tags = system_tags or []

        # Do the actual upload
        metadata = SystemMetadata(
            task=task,
            is_private=not public,
            system_name=system_name,
            dataset_name=dataset,
            sub_dataset=sub_dataset,
            metric_names=metric_names,
            source_language=source_language,
            target_language=target_language,
            dataset_split=split,
            shared_users=shared_users,
            system_tags=system_tags,
            system_details=system_details,
        )

        loaded_system_output = SystemOutputProps(
            data=encode_string_to_base64(
                json.dumps(self._convert_to_json(system_output))
            ),
            file_type="json",
        )
        if custom_dataset:
            loaded_custom_dataset = SystemOutputProps(
                data=encode_string_to_base64(
                    json.dumps(self._convert_to_json(custom_dataset))
                ),
                file_type="json",
            )
            props_with_loaded_file = SystemCreateProps(
                metadata=metadata,
                system_output=loaded_system_output,
                custom_dataset=loaded_custom_dataset,
            )
        else:
            props_with_loaded_file = SystemCreateProps(
                metadata=metadata,
                system_output=loaded_system_output,
            )
        result: System = self._default_api.systems_post(props_with_loaded_file)

        return result.to_dict()

    def evaluate_system_file(
        self,
        task: str,
        system_name: str,
        system_output_file: str,
        system_output_file_type: str | None = None,
        dataset: str | None = None,
        sub_dataset: str | None = None,
        split: str | None = None,
        custom_dataset_file: str | None = None,
        custom_dataset_file_type: str | None = None,
        metric_names: list[str] | None = None,
        source_language: str | None = None,
        target_language: str | None = None,
        system_details_file: str | None = None,
        public: bool = False,
        shared_users: list[str] | None = None,
        system_tags: list[str] | None = None,
    ) -> dict:
        """Evaluate a system output file and return a dictionary of results.

        Args:
            task: What task you will be analyzing.
            system_name: Name of the system that you are evaluating.
            system_output_file: Path to the system output file.
            system_output_file_type: File type of the system output
                (eg text/json/tsv/conll).
            dataset: A dataset name from DataLab.
            sub_dataset: A sub-dataset name from DataLab.
            split: The name of the dataset split to process.
            custom_dataset_file: The path to a custom dataset file.
            custom_dataset_file_type: File type of the custom dataset
                (eg text/json/tsv/conll)
            metric_names: The metrics to compute, leave blank for task defaults
            source_language: The language on the input side.
            target_language: The language on the output side.
            system_details_file: File of system details in JSON format.
            public: Make the evaluation results public.
            shared_users: Emails of users to share with.
            system_tags: User defined tags for the system,
                useful for searching and grouping systems
        """
        # Sanity checks
        if not (source_language or target_language):
            raise ValueError("You must specify source and/or target language")

        # Infer missing values
        task = TaskType(task)
        metric_names = metric_names or DEFAULT_METRICS[task]
        source_language = source_language or target_language
        target_language = target_language or source_language
        system_output_file_type = system_output_file_type or infer_file_type(
            system_output_file, task
        )
        custom_dataset_file_type = custom_dataset_file_type or infer_file_type(
            custom_dataset_file_type, task
        )
        shared_users = shared_users or []
        system_tags = system_tags or []

        # Read system details file
        system_details: dict = {}
        if system_details_file is not None:
            with open(system_details_file, "r") as fin:
                system_details = json.load(fin)

        # Do the actual upload
        metadata = SystemMetadata(
            task=task,
            is_private=not public,
            system_name=system_name,
            dataset_name=dataset,
            sub_dataset=sub_dataset,
            metric_names=metric_names,
            source_language=source_language,
            target_language=target_language,
            dataset_split=split,
            shared_users=shared_users,
            system_details=system_details,
            system_tags=system_tags,
        )

        loaded_system_output = SystemOutputProps(
            data=encode_file_to_base64(system_output_file),
            file_type=system_output_file_type,
        )
        if custom_dataset_file:
            loaded_custom_dataset = SystemOutputProps(
                data=encode_file_to_base64(custom_dataset_file),
                file_type=custom_dataset_file_type,
            )
            props_with_loaded_file = SystemCreateProps(
                metadata=metadata,
                system_output=loaded_system_output,
                custom_dataset=loaded_custom_dataset,
            )
        else:
            props_with_loaded_file = SystemCreateProps(
                metadata=metadata,
                system_output=loaded_system_output,
            )
        result: System = self._default_api.systems_post(props_with_loaded_file)

        return result.to_dict()

    def get_system(self, system_id: str) -> dict:
        """Get a single system by the system ID.

        Args:
            system_id: The system ID.

        Returns:
            A dictionary of information about the system.
        """
        result: System = self._default_api.systems_get_by_id(system_id)
        return result.to_dict()

    def delete_system(self, system_id: str) -> None:
        """Delete a single system.

        Args:
            system_id: The system ID.
        """
        self._default_api.systems_delete_by_id(system_id)

    def find_systems(
        self,
        system_name: str | None,
        task: str | None = None,
        dataset: str | None = None,
        sub_dataset: str | None = None,
        split: str | None = None,
        creator: str | None = None,
        shared_users: list[str] | None = None,
        system_tags: list[str] | None = None,
        page: int = 0,
        page_size: int = 20,
        sort_field: str = "created_at",
        sort_direction: Literal["desc", "asc"] = "desc",
    ) -> list[dict]:
        """Find systems by specifying a query.

        Args:
            system_name: Fuzzy match for system name.
            task: Filter by task type.
            dataset: Name of the dataset.
            sub_dataset: Name of the subdataset.
            split: Dataset split.
            creator: Email of the creator of the system.
            shared_users: Emails of users with which the system is shared.
            system_tags: User defined tags for the system,
                useful for searching and grouping systems
            page: Which page to retrieve.
            page_size: The number of items on each page. Set to 0 for all.
            sort_field: Which field to sort by. Supports `created_at` and metric names
                e.g. "Accuracy".
            sort_direction: Sort in ascending or descending order.

        Returns:
            A list of dictionaries containing system information.
        """
        # TODO(gneubig): the API is not accepting nonetype, but this seems like a bug
        result: SystemsReturn = self._default_api.systems_get(
            system_name=system_name or "",
            task=task or "",
            dataset=dataset or "",
            subdataset=sub_dataset or "",
            split=split or "",
            creator=creator or "",
            shared_users=shared_users or [],
            system_tags=system_tags or [],
            page=page,
            page_size=page_size,
            sort_field=sort_field,
            sort_direction=sort_direction,
        )
        result_list = [x.to_dict() for x in result.systems]
        return result_list

    def _benchmark_view_config_from_dict(self, view: dict) -> BenchmarkViewConfig:
        operations = view.get("operations", None)
        if operations is not None:
            operations = [
                BenchmarkOperationConfig(**operation) for operation in operations
            ]
        view.pop("operations", None)
        return BenchmarkViewConfig(operations=operations, **view)

    def _benchmark_dataset_from_dict(self, dataset: dict) -> BenchmarkDatasetConfig:
        metrics = dataset.get("metrics", None)
        if metrics is not None:
            metrics = [BenchmarkMetric(**metric) for metric in metrics]
        dataset.pop("metrics", None)
        return BenchmarkDatasetConfig(metrics=metrics, **dataset)

    def _benchmark_props_from_dict(
        self, benchmark: dict, create: bool
    ) -> BenchmarkCreateProps | BenchmarkUpdateProps:
        # views, paper, metrics, and datasets have their own
        # class types which we must explicitly construct
        # to pass type validation
        if "views" in benchmark:
            benchmark["views"] = [
                self._benchmark_view_config_from_dict(view)
                for view in benchmark["views"]
            ]

        if "paper" in benchmark:
            benchmark["paper"] = Paper(**benchmark["paper"])

        if "metrics" in benchmark:
            benchmark["metrics"] = [
                BenchmarkMetric(**metric) for metric in benchmark["metrics"]
            ]

        if "datasets" in benchmark:
            benchmark["datasets"] = [
                self._benchmark_dataset_from_dict(dataset)
                for dataset in benchmark["datasets"]
            ]

        Props = BenchmarkCreateProps if create else BenchmarkUpdateProps
        return Props(**benchmark)

    def get_benchmark(self, benchmark_id: str, by_creator: bool) -> dict:
        """Get a single benchmark by the system ID.

        Args:
            benchmark_id: The benchmark ID.

        Returns:
            A dictionary of information about the benchmark.
        """
        result: Benchmark = self._default_api.benchmark_get_by_id(
            benchmark_id, by_creator
        )
        return result.to_dict()

    def upload_benchmark(self, benchmark: dict):
        """Upload a benchmark.

        Args:
            benchmark: A dictionary. TODO(chihhao) detailed schema

        """
        props = self._benchmark_props_from_dict(benchmark, create=True)
        result: BenchmarkConfig = self._default_api.benchmark_post(props)
        return result.to_dict()

    def update_benchmark(self, benchmark_id: str, new_values: dict) -> None:
        """Update a single benchmark
        Args:
            benchmark_id: The benchmark ID.
            new_values: New values of the benchmark. TODO(chihhao) detailed schema
        """
        props = self._benchmark_props_from_dict(new_values, create=False)
        self._default_api.benchmark_update_by_id(benchmark_id, props)

    def delete_benchmark(self, benchmark_id: str) -> None:
        """Delete a single benchmark.

        Args:
            benchmark_id: The benchmark ID.
        """
        self._default_api.benchmark_delete_by_id(benchmark_id)

    # --- Pass-through API calls that will be deprecated
    def systems_post(
        self, system_create_props: SystemCreateProps, **kwargs
    ) -> Union[System, ApplyResult]:
        """Post a system using the client.

        The public function is deprecated and will be removed."""
        logging.getLogger("explainaboard_client").warning(
            "WARNING: systems_post() is deprecated and may be removed in the future."
            " Please use evaluate_file() instead."
        )
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
        return self._default_api.systems_post(props_with_loaded_file, **kwargs)

    def systems_get_by_id(self, system_id: str, **kwargs):
        """API call to get systems. Will be replaced in the future."""
        logging.getLogger("explainaboard_client").warning(
            "WARNING: systems_get_by_id() is deprecated and may be removed in the"
            " future. Please use get_system() instead."
        )
        return self._default_api.systems_get_by_id(system_id, **kwargs)

    def systems_delete_by_id(self, system_id: str, **kwargs):
        """API call to delete systems. Will be replaced in the future."""
        logging.getLogger("explainaboard_client").warning(
            "WARNING: systems_delete_by_id() is deprecated and may be removed in the"
            " future. Please use delete_system() instead."
        )
        self._default_api.systems_delete_by_id(system_id, **kwargs)

    def systems_get(self, **kwargs):
        """API call to get systems. Will be replaced in the future."""
        logging.getLogger("explainaboard_client").warning(
            "WARNING: systems_get() is deprecated and may be removed in the"
            " future. Please use get_systems() instead."
        )
        return self._default_api.systems_get(**kwargs)

    def info_get(self, **kwargs):
        """API call to get info. Will be replaced in the future."""
        return self._default_api.info_get(**kwargs)

    def user_get(self, **kwargs):
        """API call to get a user. Will be replaced in the future."""
        logging.getLogger("explainaboard_client").warning(
            "WARNING: user_get() is deprecated and may be removed in the"
            " future. Please use get_user() instead."
        )
        return self._default_api.user_get(**kwargs)

    def _convert_to_json(self, examples: list | dict) -> dict:
        if isinstance(examples, list):
            return {"examples": examples}
        if "examples" not in examples:
            raise ValueError(
                "Examples must be a list or a dictionary with an 'examples' key."
            )
        return examples
