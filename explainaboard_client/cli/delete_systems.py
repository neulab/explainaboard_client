import argparse
import sys
import traceback

from explainaboard_api_client import ApiException
import explainaboard_client
from explainaboard_client import ExplainaboardClient
from tqdm import tqdm


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A command-line tool to delete systems from the ExplainaBoard "
        "online database."
    )
    # ---- Authentication arguments
    parser.add_argument(
        "--username",
        type=str,
        default=explainaboard_client.username,
        help="Username used to sign in to ExplainaBoard. Defaults to the EB_USERNAME "
        "environment variable.",
    )
    parser.add_argument(
        "--api-key",
        type=str,
        default=explainaboard_client.api_key,
        help="API key for ExplainaBoard. Defaults to the EB_API_KEY environment "
        "variable.",
    )
    # --- Query arguments
    parser.add_argument(
        "--system-ids",
        type=str,
        nargs="+",
        required=True,
        help="The system IDs to delete",
    )
    # --- Procedural arguments
    parser.add_argument(
        "--skip-confirmation",
        action="store_true",
        help="Skip the confirmation dialog",
    )
    args = parser.parse_args()

    explainaboard_client.username = args.username
    explainaboard_client.api_key = args.api_key
    client = ExplainaboardClient()

    system_strs = []
    for system_id in tqdm(args.system_ids, desc="retrieving system info"):
        try:
            system_dict = client.get_system(system_id)

            dataset = system_dict["system_info"].get("dataset_name", "custom dataset")
            subdataset = system_dict["system_info"].get(
                "sub_dataset_name", "custom dataset"
            )
            system_strs.append(
                f"id={system_id}, "
                f'name={system_dict["system_info"]["system_name"]}, '
                f"dataset={dataset}, "
                f"subdataset={subdataset}, "
                f'created_at={str(system_dict["created_at"])}'
            )
        except ApiException:
            print(f"Could not find system ID {system_id}", file=sys.stderr)
            return
    print(
        f"--- Preparing to delete {len(system_strs)} systems:\n"
        + "\n".join(system_strs)
    )
    if not args.skip_confirmation:
        print("Are you sure? (y/N)")
        line = sys.stdin.readline()
        if line.strip() != "y":
            print("Did not receive confirmation")
            return
    deleted_systems = 0
    for system_id in args.system_ids:
        try:
            client.delete_system(system_id)
            deleted_systems += 1
        except Exception:
            print(f"Could not delete system ID {system_id}", file=sys.stderr)
            traceback.print_exc()
    print(f"Deleted {deleted_systems} system{'' if deleted_systems == 1 else 's'}")


if __name__ == "__main__":
    main()
