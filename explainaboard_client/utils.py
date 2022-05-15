import base64
from typing import Optional


def encode_file_to_base64(path: str) -> str:
    print(path)
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def generate_dataset_id(dataset_name: str, sub_dataset: Optional[str]) -> str:
    """HACK probably shouldn't expose this logic to the users"""
    sub_dataset = sub_dataset if sub_dataset else "None"
    return f"{dataset_name}---{sub_dataset}"
