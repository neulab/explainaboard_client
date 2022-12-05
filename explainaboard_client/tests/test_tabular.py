import explainaboard_client
from explainaboard_client.tests.test_utils import TestEndpointsE2E


class TestTabular(TestEndpointsE2E):
    def test_wrap_tabular_class(self):
        X_test = [[1.1, 2, "seven"], [4.1, 5, "eight"], [7.2, 8, "nine"]]
        y_test = ["a", "b", "a"]
        actual = explainaboard_client.wrap_tabular_dataset(
            X_test,
            y_test,
            column_names=["feat_a", "feat_b", "feat_c"],
            columns_to_analyze=["feat_a", "feat_c"],
        )
        expected = {
            "metadata": {
                "custom_features": {
                    "example": {
                        "feat_a": {
                            "cls_name": "Value",
                            "dtype": "float",
                            "description": "feat_a",
                        },
                        "feat_c": {
                            "cls_name": "Value",
                            "dtype": "string",
                            "description": "feat_c",
                        },
                    }
                },
                "custom_analyses": [
                    {
                        "cls_name": "BucketAnalysis",
                        "feature": "feat_a",
                        "level": "example",
                        "num_buckets": 5,
                        "method": "continuous",
                    },
                    {
                        "cls_name": "BucketAnalysis",
                        "feature": "feat_c",
                        "level": "example",
                        "num_buckets": 5,
                        "method": "discrete",
                    },
                ],
            },
            "examples": [
                {"feat_a": 1.1, "feat_b": 2, "feat_c": "seven", "true_label": "a"},
                {"feat_a": 4.1, "feat_b": 5, "feat_c": "eight", "true_label": "b"},
                {"feat_a": 7.2, "feat_b": 8, "feat_c": "nine", "true_label": "a"},
            ],
        }
        self.assertEqual(expected, actual)

    def test_wrap_tabular_reg(self):
        X_test = [[1.1, 2, "seven"], [4.1, 5, "eight"], [7.2, 8, "nine"]]
        y_test = [0.5, 0.7, 0.9]
        actual = explainaboard_client.wrap_tabular_dataset(
            X_test,
            y_test,
            column_names=["feat_a", "feat_b", "feat_c"],
            columns_to_analyze=["feat_a", "feat_c"],
            task_type="regression",
        )
        expected = {
            "metadata": {
                "custom_features": {
                    "example": {
                        "feat_a": {
                            "cls_name": "Value",
                            "dtype": "float",
                            "description": "feat_a",
                        },
                        "feat_c": {
                            "cls_name": "Value",
                            "dtype": "string",
                            "description": "feat_c",
                        },
                    }
                },
                "custom_analyses": [
                    {
                        "cls_name": "BucketAnalysis",
                        "feature": "feat_a",
                        "level": "example",
                        "num_buckets": 5,
                        "method": "continuous",
                    },
                    {
                        "cls_name": "BucketAnalysis",
                        "feature": "feat_c",
                        "level": "example",
                        "num_buckets": 5,
                        "method": "discrete",
                    },
                ],
            },
            "examples": [
                {"feat_a": 1.1, "feat_b": 2, "feat_c": "seven", "true_value": 0.5},
                {"feat_a": 4.1, "feat_b": 5, "feat_c": "eight", "true_value": 0.7},
                {"feat_a": 7.2, "feat_b": 8, "feat_c": "nine", "true_value": 0.9},
            ],
        }
        self.assertEqual(expected, actual)
