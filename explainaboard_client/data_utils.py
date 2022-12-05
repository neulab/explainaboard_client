from __future__ import annotations

from typing import Literal


def wrap_tabular_dataset(
    X_test,
    y_test,
    column_names: list[str],
    columns_to_analyze: list[str],
    task_type: Literal["classification", "regression"] = "classification",
) -> dict:
    """Wrap a tabular dataset into a dictionary.

    Args:
        X_test: The test dataset.
        y_test: The test labels.
        column_names: The column names of the dataset.
        columns_to_analyze: The columns to analyze.

    Returns:
        A dictionary containing the dataset.
    """
    if len(X_test[0]) != len(column_names):
        raise ValueError(
            f"The number of columns in the dataset {len(X_test[0])} does not match "
            f"the number of column names {len(column_names)}."
        )

    output_type = "label" if task_type == "classification" else "value"
    examples = []
    X_test = X_test.tolist() if not isinstance(X_test, list) else X_test
    y_test = y_test.tolist() if not isinstance(y_test, list) else y_test
    for x, y in zip(X_test, y_test):
        data = {k: v for k, v in zip(column_names, x)}
        data[f"true_{output_type}"] = y
        examples.append(data)
    column_map = {k: v for v, k in enumerate(column_names)}
    for column in columns_to_analyze:
        if column not in column_map:
            raise ValueError(f"Column {column} not found in the dataset.")
    # metadata: dict[str, dict[str, dict] | list[dict]] = {}
    custom_features: dict[str, dict] = {"example": {}}
    custom_analyses = []
    for column in columns_to_analyze:
        first_val = examples[0][column]
        if type(first_val) == float:
            dtype = "float"
            method = "continuous"
        elif type(first_val) == int:
            dtype = "int"
            method = "continuous"
        else:
            dtype = "string"
            method = "discrete"
        custom_features["example"][column] = {
            "cls_name": "Value",
            "dtype": dtype,
            "description": column,
        }
        custom_analyses.append(
            {
                "cls_name": "BucketAnalysis",
                "feature": column,
                "level": "example",
                "num_buckets": 5,
                "method": method,
            }
        )
    metadata = {"custom_features": custom_features, "custom_analyses": custom_analyses}
    return {"metadata": metadata, "examples": examples}


def wrap_tabular_predictions(
    y_pred,
    task_type: Literal["classification", "regression"] = "classification",
) -> list[dict]:
    output_type = "label" if task_type == "classification" else "value"
    return [{f"predicted_{output_type}": y} for y in y_pred]
