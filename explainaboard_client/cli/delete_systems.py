import argparse
import sys
import traceback

from explainaboard_api_client import ApiException
from explainaboard_api_client.model.systems_return import SystemsReturn
from explainaboard_client import Config, ExplainaboardClient
from tqdm import tqdm


def main():

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A command-line tool to delete systems from the ExplainaBoard "
        "online database."
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
        "--system_ids",
        type=str,
        nargs="+",
        required=True,
        help="The system IDs to delete",
    )
    # --- Procedural arguments
    parser.add_argument(
        "--skip_confirmation",
        action="store_true",
        help="Skip the confirmation dialog",
    )
    args = parser.parse_args()

    client_config = Config(
        args.email,
        args.api_key,
        args.server,
    )
    client = ExplainaboardClient(client_config)
    try:
        system_strs = []
        for system_id in tqdm(args.system_ids, desc="retrieving system info"):
            kwargs = {"system_id": system_id}
            try:
                system: SystemsReturn = client.systems_system_id_get(**kwargs)
                system_dict = system.to_dict()
                system_strs.append(
                    f"id={system_id}, "
                    f'name={system_dict["system_info"]["system_name"]}, '
                    f'dataset={system_dict["system_info"]["dataset_name"]}, '
                    f'subdataset={system_dict["system_info"]["sub_dataset_name"]}, '
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
        for system_id in args.system_ids:
            client.systems_system_id_delete(system_id)
        print(f"Deleted {len(system_strs)} systems")
    except Exception:
        traceback.print_exc()
        print("Failed to delete systems")


if __name__ == "__main__":
    main()
