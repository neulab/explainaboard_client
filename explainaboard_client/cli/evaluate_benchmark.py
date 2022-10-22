import argparse
import json
import os
import time

from explainaboard_api_client.model.system import System
from explainaboard_api_client.model.system_create_props import SystemCreateProps
from explainaboard_api_client.model.system_metadata import SystemMetadata
from explainaboard_api_client.model.system_output_props import SystemOutputProps
import explainaboard_client
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
    # ---- Authentication arguments
    parser.add_argument(
        "--username",
        type=str,
        help="Username used to sign in to ExplainaBoard. Defaults to the EB_USERNAME "
        "environment variable.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        help="API key for ExplainaBoard. Defaults to the EB_API_KEY environment "
        "variable.",
    )

    parser.add_argument(
        "--public", action="store_true", help="Make the evaluation results public"
    )

    parser.add_argument("--system-name", type=str, help="system_name")

    parser.add_argument("--benchmark", type=str, help="benchmark config")

    parser.add_argument(
        "--system-outputs", type=str, nargs="+", help="benchmark config"
    )

    parser.add_argument(
        "--system-details", type=str, help="File of system details in JSON format"
    )

    parser.add_argument(
        "--shared-users", type=str, nargs="+", help="Emails of users to share with"
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
        explainaboard_client.username = (
            args.username
            if args.username is not None
            else os.environ.get("EB_USERNAME")
        )
        explainaboard_client.api_key = (
            args.api_key if args.api_key is not None else os.environ.get("EB_API_KEY")
        )
        client = ExplainaboardClient()

        result: System = client.systems_post(create_props)
        try:
            sys_id = result.system_id
            client.get_system(sys_id)
            print(f"evaluated system {args.system_name} with ID {sys_id}")
        except Exception:
            print(f"failed to evaluate system {args.system_name}")


if __name__ == "__main__":
    main()
