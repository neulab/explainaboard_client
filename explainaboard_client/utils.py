import base64
from datetime import datetime
from typing import Any, Optional


def encode_file_to_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def encode_string_to_base64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("utf-8")


def generate_dataset_id(dataset_name: str, sub_dataset: Optional[str]) -> str:
    """HACK probably shouldn't expose this logic to the users"""
    if not dataset_name:
        raise ValueError(
            "dataset_name cannot be None or empty. If you are "
            "using a custom dataset, please remove the dataset argument."
        )
    sub_dataset = sub_dataset if sub_dataset else "None"
    return f"{dataset_name}---{sub_dataset}"


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
