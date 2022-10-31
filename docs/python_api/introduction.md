# Accessing ExplainaBoard through Python

You can programmatically evaluate systems using ExplainaBoard using calls to the
ExplainaBoard client Python API. See the description below, or the examples in the
[API example code](/example/api) directory.

## Evaluating System Output Files

In the most common case, you will have a system output (e.g. 
[sst2-lstm-output.txt](/example/data/sst2-lstm-output.txt)) that is on one of the
[datasets supported by ExplainaBoard](https://explainaboard.inspiredco.ai/datasets),
such as `sst2`.

If this is the case, you can perform evaluation with the following code.

```python
import os
import explainaboard_client

# Set up your environment
explainaboard_client.username = os.environ['EB_USERNAME']
explainaboard_client.api_key = os.environ['EB_API_KEY']
client = explainaboard_client.ExplainaboardClient()

# Do the evaluation
evaluation_result = client.evaluate_system_file(
    task='text-classification',
    system_name='text-classification-test',
    system_output_file='example/data/sst2-lstm-output.txt',
    system_output_file_type='text',
    dataset='sst2',
    split='test',
    source_language='en',
)
```

If you want to just print out the system name, ID, and evaluation results, you can
run the following code.
```python
print(f'Successfully submitted system!\n'
      f'Name: {evaluation_result["system_name"]}\n'
      f'ID: {evaluation_result["system_id"]}')
results = evaluation_result['results']['example'].items()
for metric_name, value in results:
    print(f'{metric_name}: {value:.4f}')
```

Alternatively, you can dump all of the results and process them in any way you want.
```python
import json
print(json.dumps(evaluation_result, indent=2, default=str))
```

## Evaluating Outputs from Memory

If you don't want to bother reading data from a file, you can also directly evaluate
files from memory. For example, do the same as above, but pass in a list of
dictionaries containing the system outputs:
```python
my_labels = [
    {'predicted_label': 'positive'},
    {'predicted_label': 'negative'},
    ...
]
evaluation_result = client.evaluate_system(
    task='text-classification',
    system_name='text-classification-test',
    system_output=my_labels,
    dataset='sst2',
    split='test',
    source_language='en',
)
```

Note that the exact format of the dictionary will depend on the task. You can find
the appropriate format for your task by going to the
[ExplainaBoard task file formats](https://github.com/neulab/ExplainaBoard/blob/main/docs/task_file_formats.md)
page and looking for the "JSON" format, which should mirror what you need to pass in.

## Finding Systems

Finding systems is relatively simple. You call the `find_systems()` function of client
and specify particular filters that you would like to use to filter the systems.
```python
found_systems = client.find_systems(system_name="test")
```
Please reference the API docstrings for all of the possible options.

## Deleting Systems

In order to delete systems you call:
```python
client.delete_system(sys_id)
```
where `sys_id` is the system ID (a hash value).

