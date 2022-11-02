import argparse
import json
import os
import traceback

import explainaboard_client
from explainaboard_client import ExplainaboardClient
from explainaboard_client.utils import sanitize_for_json


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A command-line tool to find systems from the ExplainaBoard online "
        "database, and output system info in JSON format."
    )
    # --- Authentication arguments
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
    # --- Query arguments
    parser.add_argument(
        "--system-name",
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
        "--shared-users",
        type=str,
        nargs="+",
        help="Emails of users with which the system is shared",
    )
    # ---- Display settings
    parser.add_argument(
        "--output-format",
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
        "--page-size",
        type=int,
        default=20,
        help="The number of items on each page. Set to 0 for all.",
    )
    parser.add_argument(
        "--sort-field",
        type=str,
        help="Which field to sort by. Supports `created_at` and metric names "
        "(e.g. Accuracy)",
    )
    parser.add_argument(
        "--sort-direction",
        type=str,
        default="desc",
        choices=["desc", "asc"],
        help="Sort in ascending or descending order",
    )
    args = parser.parse_args()

    explainaboard_client.username = (
        args.username if args.username is not None else os.environ.get("EB_USERNAME")
    )
    explainaboard_client.api_key = (
        args.api_key if args.api_key is not None else os.environ.get("EB_API_KEY")
    )
    client = ExplainaboardClient()
    try:
        system_list: list[dict] = client.find_systems(
            system_name=args.system_name,
            task=args.task,
            dataset=args.dataset,
            sub_dataset=args.subdataset,
            split=args.split,
            creator=args.creator,
            shared_users=args.shared_users,
            page=args.page,
            page_size=args.page_size,
            sort_field=args.sort_field,
            sort_direction=args.sort_direction,
        )
        system_list = [sanitize_for_json(x) for x in system_list]
        if args.output_format == "json":
            print(json.dumps(system_list))
        else:
            # Get types of metrics
            # each item is (analysis_level, metric_name)
            metric_names: set[tuple[str, str]] = set()
            for system in system_list:
                for level, metric in system["results"].items():
                    metric_names = metric_names.union(
                        {(level, metric_name) for metric_name in metric}
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
            ] + [f"{level}.{metric_name}" for level, metric_name in metric_list]
            print("\t".join(headings))
            for system in system_list:
                metrics = [
                    system["results"].get(level, {}).get(metric_name)
                    for level, metric_name in metric_list
                ]
                metric_strs = [str(x) if x else "" for x in metrics]
                dataset = system.get("dataset", {})
                system_data = [
                    system["system_id"],
                    system["system_name"],
                    system["task"],
                    dataset.get("dataset_name", ""),
                    dataset.get("sub_dataset", ""),
                    dataset.get("split", ""),
                    system["source_language"],
                    system["target_language"],
                    system["creator"],
                    system["created_at"],
                ] + metric_strs
                print("\t".join(system_data))

    except Exception:
        traceback.print_exc()
        print("failed to query systems")


if __name__ == "__main__":
    main()
