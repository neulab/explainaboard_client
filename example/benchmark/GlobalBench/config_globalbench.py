globalbench_config = {
    "id": "global_bench_example",
    "is_private": False,
    "shared_users": ["explainaboard@gmail.com"],
    "name": "Global Benchmark",
    "parent": "",
    "description": "",
    "views": [
        {
            "name": "TODO",
            "operations": [{"op": "mean", "group_by": ["sub_dataset"]}],
        }
    ],
    # == OPTIONAL FIELDS ==
    # Specify "abstract" to indicate this doesn't
    # fully specify a benchmark
    "type": "",
    # Please contact us and send us your logo.
    # We will add it to our image store and update the link.
    "logo": "",
    "contact": "explainaboard@gmail.com",
    "homepage": "https://github.com/neulab/globalbench",
    "paper": {
        # REQUIRED if paper is not None
        "title": "GlobalBench: A Benchmark for Global Progress in Natural Language Processing",
        "url": "TODO",
    },
    "metrics": [
        {
            # REQUIRED for each metrics element
            "name": "ExampleMetric",
            # OPTIONAL
            "weight": 1.0,
            "default": 1.0,
        }
    ],
    "datasets": [
        {
            # REQUIRED for each datasets element
            "dataset_name": "example_dataset",
            # OPTIONAL
            "sub_dataset": "example_sub_dataset",
            "split": "test",
            "metrics": [
                {
                    # REQUIRED for each metrics element
                    "name": "ExampleMetric",
                    # OPTIONAL
                    "weight": 1.0,
                    "default": 1.0,
                }
            ],
        }
    ],
    "system_query": {
        "task_name": "example-task",
    },
    "default_views": ["Example View"],
}
