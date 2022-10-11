import argparse
import json
import os
import time

from explainaboard_api_client.model.system import System
from explainaboard_api_client.model.system_create_props import SystemCreateProps
from explainaboard_api_client.model.system_metadata import SystemMetadata
from explainaboard_api_client.model.system_output_props import SystemOutputProps
from explainaboard_client import ExplainaboardClient
from explainaboard_client.utils import generate_dataset_id


def validate_outputs(system_outputs):
    for pth in system_outputs:
        if not os.path.basename(pth).split(".")[0].split("_")[0].isdigit():
            raise ValueError(
                f"system output file name: {pth}  should"
                f" start with a number,"
                "for example: 8.json"
            )
    return True


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A command-line tool to submit to benchmarks "
        "on the ExplainaBoard web interface."
    )
    parser.add_argument(
        "--username",
        type=str,
        required=True,
        help="Email address used to sign in to ExplainaBoard",
    )
    parser.add_argument("--api_key", type=str, required=True, help="Your API key")

    parser.add_argument(
        "--public", action="store_true", help="Make the evaluation results public"
    )

    parser.add_argument("--system_name", type=str, help="system_name")

    parser.add_argument("--benchmark", type=str, help="benchmark config")

    parser.add_argument(
        "--system_outputs", type=str, nargs="+", help="benchmark config"
    )

    parser.add_argument(
        "--system_details", type=str, help="File of system details in JSON format"
    )

    parser.add_argument(
        "--shared_users", type=str, nargs="+", help="Emails of users to share with"
    )
    parser.add_argument(
        "--environment",
        type=str,
        required=False,
        default="main",
        choices=["main", "staging", "local"],
        help='Which environment to use, "main" should be sufficient',
    )
    args = parser.parse_args()

    benchmark = args.benchmark
    with open(benchmark, "r") as f:
        benchmark_config = json.load(f)

    system_outputs = args.system_outputs

    if validate_outputs(system_outputs):
        system_outputs.sort(
            key=lambda system_path: int(
                os.path.basename(system_path).split(".")[0].split("_")[0]
            )
        )
    else:
        raise ValueError("System output file names should start with number")

    shared_users = args.shared_users or []
    # Read system details file
    system_details = {}
    if args.system_details:
        with open(args.system_details, "r") as fin:
            system_details = json.load(fin)

    for idx, dataset_info in enumerate(benchmark_config["datasets"]):
        if idx > 0:
            time.sleep(5)
        dataset_name = dataset_info["dataset_name"]
        sub_dataset = dataset_info["sub_dataset"]
        dataset_split = dataset_info["dataset_split"]
        metric_names = [metric_dict["name"] for metric_dict in dataset_info["metrics"]]
        task = dataset_info["task"]

        source_language = (
            "en"
            if "source_language" not in dataset_info.keys()
            else dataset_info["source_language"]
        )

        target_language = (
            "en"
            if "target_language" not in dataset_info.keys()
            else dataset_info["target_language"]
        )

        output_file_type = dataset_info["output_file_type"]

        # Do the actual upload
        system_output = SystemOutputProps(
            data=system_outputs[idx],
            file_type=output_file_type,
        )

        metadata = SystemMetadata(
            task=task,
            is_private=not args.public,
            system_name=args.system_name,
            metric_names=metric_names,
            source_language=source_language,
            target_language=target_language,
            dataset_metadata_id=generate_dataset_id(dataset_name, sub_dataset),
            dataset_split=dataset_split,
            shared_users=shared_users,
            system_details=system_details,
        )

        create_props = SystemCreateProps(
            metadata=metadata, system_output=system_output, custom_datset=None
        )
        client = ExplainaboardClient(
            username=args.username, api_key=args.api_key, environment=args.environment
        )

        result: System = client.systems_post(create_props)
        try:
            sys_id = result.system_id
            client.get_system(sys_id)
            print(f"evaluated system {args.system_name} with ID {sys_id}")
        except Exception:
            print(f"failed to evaluate system {args.system_name}")


if __name__ == "__main__":
    main()
