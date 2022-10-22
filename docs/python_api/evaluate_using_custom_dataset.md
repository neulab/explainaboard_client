# Evaluating using Custom Datasets

This document explains how to evaluate your system on your datasets that are not in DataLab.

* Step 1: Prepare `dataset` and `system output` separately
You need first preprocess your dataset and system output into certain formats as
 suggested in this [doc](https://github.com/neulab/ExplainaBoard/blob/main/docs/task_file_formats.md).

FAQ: what do `dataset` and `system output` mean? check [this](https://github.com/neulab/ExplainaBoard/blob/main/docs/concepts_about_system_analysis.md).


* Step 2: Use `client.evaluate_system_file` or `client.evaluate_system` to process the above files


## Example
We will illustrate the above process using the `machine-translation` task as an example.

* from the [doc](https://github.com/neulab/ExplainaBoard/blob/main/docs/task_file_formats.md) we see
that for the dataset file, we can preprocess it into `tsv` or `json` format, and for the output file, 
`json` and `text` are allowed. 
* Suppose that you process the dataset and system output files into
 `tsv` (e.g., [`dataset.tsv`](../example/data/machine_translation/dataset.tsv))
  and
  `text` (e.g., [`system_output.txt`](../example/data/machine_translation/system_output.txt))
  accordingly. You can then use the
following code to evaluate your system

```python
import os
import explainaboard_client

# Set up your environment
explainaboard_client.username = os.environ['EB_USERNAME']
explainaboard_client.api_key = os.environ['EB_API_KEY']
client = explainaboard_client.ExplainaboardClient()

# Do the evaluation
evaluation_result = client.evaluate_system_file(
    task='machine-translation',
    system_name="my_first_system",
    system_output_file="../example/data/machine_translation/system_output.txt",
    system_output_file_type="text",
    custom_dataset_file="../example/data/machine_translation/dataset.tsv",
    custom_dataset_file_type="tsv",
    split="test",
    source_language="cs",
    target_language="en",
    metric_names = ["bleu","comet"],
)

# print(evaluation_result)
```

* then you can analyze your results either by passing the python dictionary `evaluation_result` or
interacting with the [web platform](https://explainaboard.inspiredco.ai/systems) 



