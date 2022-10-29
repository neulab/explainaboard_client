import os

import explainaboard_client

# Set up your environment
explainaboard_client.username = os.environ["EB_USERNAME"]
explainaboard_client.api_key = os.environ["EB_API_KEY"]
client = explainaboard_client.ExplainaboardClient()

# Do the evaluation
evaluation_result = client.evaluate_system_file(
    task="text-classification",
    system_name="text-classification-test",
    system_output_file="../data/sst2-lstm-output.txt",
    system_output_file_type="text",
    dataset="sst2",
    split="test",
    source_language="en",
)

# Print out rudimentary results
print(
    f"Successfully submitted system!\n"
    f'Name: {evaluation_result["system_name"]}\n'
    f'ID: {evaluation_result["system_id"]}'
)
overall_results = evaluation_result["overall_metrics"]["example"].values()
for result in overall_results:
    print(
        f'{result["metric_name"]}: {result["value"]:.4f} '
        f'[{result["confidence_score_low"]:.4f}, '
        f'{result["confidence_score_high"]:.4f}]'
    )

# Do additional processing/analysis on evaluation_result
# print(json.dumps(evaluation_result, indent=2, default=str))
