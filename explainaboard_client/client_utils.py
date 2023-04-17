import base64
from datetime import datetime
from distutils.util import strtobool
import os
import sys
from typing import Any, Optional

from explainaboard_client.exceptions import APIVersionMismatchException


def encode_file_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def encode_string_to_base64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def sanitize_for_json(input_obj: Any) -> Any:
    if hasattr(input_obj, "to_dict"):
        return sanitize_for_json(getattr(input_obj, "to_dict")())
    elif isinstance(input_obj, dict):
        return {k: sanitize_for_json(v) for k, v in input_obj.items()}
    elif isinstance(input_obj, list):
        return [sanitize_for_json(v) for v in input_obj]
    elif isinstance(input_obj, datetime):
        return str(input_obj)
    else:
        return input_obj


def prompt_for_auto_upgrade_and_exit(exception: APIVersionMismatchException):
    print(f"{exception.message}\n" "Would you like an auto-upgrade? [y/n]")
    required_package = f"{exception.package}=={exception.required_version}"

    if strtobool(input()):
        print(f"Installing {required_package}")
        os.system(f"pip install {required_package}")
        print("Installation completed.")
    else:
        print("Please perform the upgrade manually.")
    print("Exiting the client.")
    sys.exit(0)
