import sys

from explainaboard_client.cli import evaluate_benchmark

if __name__ == "__main__":
    print(
        "WARNING: The upload_benchmark command is deprecated and will be removed in "
        "a future release. Please use the evaluate_benchmark command instead.",
        file=sys.stderr,
    )
    evaluate_benchmark.main()
