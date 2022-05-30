import argparse
import json
import traceback

from explainaboard_api_client.model.system import System
from explainaboard_api_client.model.systems_return import SystemsReturn
from explainaboard_client import Config, ExplainaboardClient
from explainaboard_client.utils import sanitize_for_json


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A command-line tool to find systems from the ExplainaBoard online "
        "database, and output system info in JSON format."
    )
    # --- Authentication arguments
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
    # --- Query arguments
    parser.add_argument(
        "--system_name",
        type=str,
        help="Fuzzy match for system name",
    )
    parser.add_argument(
        "--task",
        type=str,
        help="Filter by task type",
    )
    parser.add_argument(
        "--dataset",
        type=str,
        help="Name of the dataset",
    )
    parser.add_argument(
        "--subdataset",
        type=str,
        help="Name of the subdataset",
    )
    parser.add_argument(
        "--split",
        type=str,
        help="Dataset split",
    )
    parser.add_argument(
        "--creator",
        type=str,
        help="Email of the creator of the system",
    )
    parser.add_argument(
        "--shared_users",
        type=str,
        nargs="+",
        help="Emails of users with which the system is shared",
    )
    # ---- Display settings
    parser.add_argument(
        "--output_format",
        type=str,
        default="tsv",
        choices=["tsv", "json"],
        help="What format to output in",
    )
    parser.add_argument(
        "--page",
        type=int,
        default=0,
        help="Which page to retrieve",
    )
    parser.add_argument(
        "--page_size",
        type=int,
        default=20,
        help="The number of items on each page. Set to 0 for all.",
    )
    parser.add_argument(
        "--sort_field",
        type=str,
        help="Which field to sort by. Supports `created_at` and metric names "
        "(e.g. Accuracy)",
    )
    parser.add_argument(
        "--sort_direction",
        type=str,
        default="desc",
        choices=["desc", "asc"],
        help="Sort in ascending or descending order",
    )
    args = parser.parse_args()

    client_config = Config(
        args.email,
        args.api_key,
        args.server,
    )
    client = ExplainaboardClient(client_config)
    kwargs: dict = {
        k: v
        for k, v in vars(args).items()
        if (v is not None and k not in {"email", "api_key", "server", "output_format"})
    }
    try:
        systems: SystemsReturn = client.systems_get(**kwargs)
        system_list: list[System] = [
            sanitize_for_json(x.to_dict()) for x in systems.systems
        ]
        if args.output_format == "json":
            print(json.dumps(system_list))
        else:
            # Get types of metrics
            metric_names = set()
            for system in system_list:
                metric_names = metric_names.union(
                    system["system_info"]["results"]["overall"].keys()
                )
            metric_list = list(metric_names)
            # Print headings
            headings = [
                "ID",
                "Name",
                "Task",
                "Dataset",
                "Sub-dataset",
                "Split",
                "Input Language",
                "Output Language",
                "Creator",
                "Created At",
            ] + metric_list
            print("\t".join(headings))
            for system in system_list:
                metrics = [
                    system["system_info"]["results"]["overall"].get(x, None)
                    for x in metric_list
                ]
                metric_strs = [str(x["value"]) if x else "" for x in metrics]
                system_data = [
                    system["system_id"],
                    system["system_info"]["system_name"],
                    system["system_info"]["task_name"],
                    system["system_info"]["dataset_name"],
                    system["system_info"].get("sub_dataset_name", ""),
                    system["system_info"]["dataset_split"],
                    system["system_info"]["source_language"],
                    system["system_info"]["target_language"],
                    system["creator"],
                    system["created_at"],
                ] + metric_strs
                print("\t".join(system_data))

    except Exception:
        traceback.print_exc()
        print("failed to query systems")


if __name__ == "__main__":
    main()
