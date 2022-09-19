import sys

from explainaboard_client.cli import evaluate_system

if __name__ == "__main__":
    print(
        "WARNING: The upload_system command is deprecated and will be removed in a "
        "future release. Please use the evaluate_system command instead.",
        file=sys.stderr,
    )
    evaluate_system.main()
