import argparse
import json

from explainaboard_api_client.model.system import System
from explainaboard_api_client.model.system_create_props import SystemCreateProps
from explainaboard_api_client.model.system_metadata import SystemMetadata
from explainaboard_api_client.model.system_output_props import SystemOutputProps
from explainaboard_client import Config, ExplainaboardClient
from explainaboard_client.tasks import (
    DEFAULT_METRICS,
    FileType,
    infer_file_type,
    TaskType,
)
from explainaboard_client.utils import generate_dataset_id


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A command-line tool to upload system "
        "to the ExplainaBoard web interface."
    )
    # ---- Authentication arguments
    parser.add_argument(
        "--email",
        type=str,
        required=True,
        help="Email address used to sign in to ExplainaBoard",
    )
    parser.add_argument("--api_key", type=str, required=True, help="Your API key")
    parser.add_argument(
        "--server",
        type=str,
        required=False,
        default="main",
        choices=["main", "staging", "local"],
        help='Which server to upload to, "main" should be sufficient',
    )
    # ---- System info
    parser.add_argument(
        "--task",
        type=str,
        required=True,
        choices=TaskType.list(),
        help="What task you will be analyzing",
    )
    parser.add_argument(
        "--system_name",
        type=str,
        required=True,
        help="Name of the system that you are uploading",
    )
    parser.add_argument(
        "--system_output",
        type=str,
        required=True,
        help="Path to the system output file",
    )
    parser.add_argument(
        "--output_file_type",
        type=str,
        choices=FileType.list(),
        help="File type of the system output (eg text/json/tsv/conll)",
    )
    dataset_group = parser.add_mutually_exclusive_group(required=True)
    dataset_group.add_argument(
        "--dataset", type=str, help="A dataset name from DataLab"
    )
    parser.add_argument(
        "--sub_dataset",
        type=str,
        required=False,
        help="A sub-dataset name from DataLab",
    )
    parser.add_argument(
        "--split",
        type=str,
        required=False,
        default="test",
        help="The name of the dataset split to process",
    )
    dataset_group.add_argument(
        "--custom_dataset", type=str, help="The path to a custom dataset file"
    )
    parser.add_argument(
        "--custom_dataset_file_type",
        type=str,
        required=False,
        choices=FileType.list(),
        help="File type of the custom dataset (eg text/json/tsv/conll)",
    )
    parser.add_argument(
        "--metric_names",
        type=str,
        nargs="+",
        required=False,
        help="The metrics to compute, leave blank for task defaults",
    )
    parser.add_argument(
        "--source_language", type=str, help="The language on the input side"
    )
    parser.add_argument(
        "--target_language", type=str, help="The language on the output side"
    )
    parser.add_argument(
        "--system_details", type=str, help="File of system details in JSON format"
    )
    parser.add_argument(
        "--public", action="store_true", help="Make the uploaded system public"
    )
    parser.add_argument(
        "--shared_users", type=str, nargs="+", help="Emails of users to share with"
    )
    args = parser.parse_args()

    # Sanity checks
    if not (args.source_language or args.target_language):
        raise ValueError("You must specify source and/or target language")

    # Infer missing values
    task = TaskType(args.task)
    metric_names = args.metric_names or DEFAULT_METRICS[args.task]
    source_language = args.source_language or args.target_language
    target_language = args.target_language or args.source_language
    output_file_type = args.output_file_type or infer_file_type(
        args.system_output, task
    )
    custom_dataset_file_type = args.custom_dataset_file_type or infer_file_type(
        args.custom_dataset_file_type, task
    )
    shared_users = args.shared_users or []

    # Read system details file
    system_details = {}
    if args.system_details:
        with open(args.system_details, "r") as fin:
            system_details = json.load(fin)

    # Do the actual upload
    system_output = SystemOutputProps(
        data=args.system_output,
        file_type=output_file_type,
    )
    metadata = SystemMetadata(
        task=args.task,
        is_private=not args.public,
        system_name=args.system_name,
        metric_names=metric_names,
        source_language=source_language,
        target_language=target_language,
        dataset_metadata_id=generate_dataset_id(args.dataset, args.sub_dataset),
        dataset_split=args.split,
        shared_users=shared_users,
        system_details=system_details,
    )
    custom_dataset = None
    if args.custom_dataset:
        custom_dataset = SystemOutputProps(
            data=args.custom_dataset,
            file_type=custom_dataset_file_type,
        )
    create_props = SystemCreateProps(
        metadata=metadata, system_output=system_output, custom_datset=custom_dataset
    )
    client_config = Config(
        args.email,
        args.api_key,
        args.server,
    )
    client = ExplainaboardClient(client_config)

    result: System = client.systems_post(create_props)
    try:
        sys_id = result.system_id
        client.systems_system_id_get(sys_id)
        print(f"successfully posted system {args.system_name} with ID {sys_id}")
    except Exception:
        print(f"failed to post system {args.system_name}")


if __name__ == "__main__":
    main()
