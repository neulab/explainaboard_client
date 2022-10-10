import argparse
import json
import os
import time

from explainaboard_client import Config, ExplainaboardClient

# How long to sleep between submissions
_SLEEP_BETWEEN_SUBMISSIONS = 5


def _validate_and_sort_outputs(system_output_files: list[str]) -> None:
    for pth in system_output_files:
        if not os.path.basename(pth).split(".")[0].split("_")[0].isdigit():
            raise ValueError(
                f"system output file name: {pth}  should"
                f" start with a number,"
                "for example: 8.json"
            )
    system_output_files.sort(
        key=lambda system_path: int(
            os.path.basename(system_path).split(".")[0].split("_")[0]
        )
    )


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A command-line tool to submit to benchmarks "
        "on the ExplainaBoard web interface."
    )
    parser.add_argument(
        "--email",
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
        "--system_output_files", type=str, nargs="+", help="The system output files."
    )

    parser.add_argument(
        "--system_details_file", type=str, help="File of system details in JSON format"
    )

    parser.add_argument(
        "--shared_users", type=str, nargs="+", help="Emails of users to share with"
    )
    parser.add_argument(
        "--server",
        type=str,
        required=False,
        default="main",
        choices=["main", "staging", "local"],
        help='Which server to use, "main" should be sufficient',
    )
    args = parser.parse_args()

    client_config = Config(
        args.email,
        args.api_key,
        args.server,
    )
    client = ExplainaboardClient(client_config)
    frontend = client_config.get_env_host_map()[args.server].frontend

    benchmark = args.benchmark
    with open(benchmark, "r") as f:
        benchmark_config = json.load(f)

    system_output_files = args.system_output_files
    _validate_and_sort_outputs(system_output_files)

    shared_users = args.shared_users or []

    for idx, dataset_info in enumerate(benchmark_config["datasets"]):
        if idx > 0:
            time.sleep(_SLEEP_BETWEEN_SUBMISSIONS)

        source_language = dataset_info.get("source_language", "en")
        target_language = dataset_info.get("target_language", "en")
        metric_names = [metric_dict["name"] for metric_dict in dataset_info["metrics"]]

        result = client.evaluate_system_file(
            system_output_file=system_output_files[idx],
            system_output_file_type=dataset_info["output_file_type"],
            task=dataset_info["task"],
            public=args.public,
            system_name=args.system_name,
            metric_names=metric_names,
            source_language=source_language,
            target_language=target_language,
            dataset=dataset_info["dataset_name"],
            sub_dataset=dataset_info.get("sub_dataset"),
            split=dataset_info.get("dataset_split"),
            shared_users=shared_users,
            system_details_file=args.system_details_file,
        )

        sys_id = result["system_id"]
        try:
            client.systems_get_by_id(sys_id)
            print(
                f"successfully evaluated system {args.system_name} on"
                f" {system_output_files[idx]} with ID {sys_id}\n"
                f"view it at {frontend}/systems?system_id={sys_id}\n"
            )
        except Exception:
            print(
                f"failed to evaluate system {args.system_name} on"
                f" {system_output_files[idx]}"
            )


if __name__ == "__main__":
    main()
