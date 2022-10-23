# Text Classification

This doc detail how to use simple python code to evaluate systems of text 
classification tasks in different scenarios.

## Table of Contents

* [Load Custom Dataset from Memory](#load-custom-dataset-from-memory)
* [Load Custom Dataset from Files](#load-custom-dataset-from-Files)
* [Load DataLab Dataset from Memory](#load-dataLab-dataset-from-memory)
* [Load DataLab Dataset from Files](#load-dataLab-dataset-from-files)


## Load Custom Dataset from Memory

```python
import os
import explainaboard_client

# Set up your environment
explainaboard_client.username = os.environ['EB_USERNAME']
explainaboard_client.api_key = os.environ['EB_API_KEY']
client = explainaboard_client.ExplainaboardClient()

custom_data = [
    {"text":"this is a good movie", "true_label":"positive"},
    {"text":"this movie is too long", "true_label":"negative"},
]

system_output = [
    {"predicted_label":"positive"},
    {"predicted_label":"negative"}
]


# Do the evaluation
evaluation_result = client.evaluate_system(
    task="text-classification",
    system_name="my-first-system",
    system_output=system_output,
    custom_dataset=custom_data,
    split="test",
    source_language="en",
    system_details={},
)

# print(evaluation_result)
# print(evaluation_result['system_info']['results']['overall'][0])

```
Note:
* The dataset and system output should be preprocessed into `List[Dict]`, where
    * for the dataset, the dictionary keys are: `text` and `true_label`
    * for the system output, the dictionary key is: `predicted_label`
   
* After running the above code, you can browse and interactively analyze your system's 
result [here](https://explainaboard.inspiredco.ai/systems)



## Load Custom Dataset from Files

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
    system_output_file='../../example/data/text_classification/sst2-lstm-output.txt',
    system_output_file_type='text',
    custom_dataset_file='../../example/data/text_classification/sst2-dataset.tsv',
    custom_dataset_file_type='tsv',
    split='test',
    source_language='en',
)
```


## Load DataLab Dataset from Memory


```python
import os
import explainaboard_client

# Set up your environment
explainaboard_client.username = os.environ['EB_USERNAME']
explainaboard_client.api_key = os.environ['EB_API_KEY']
client = explainaboard_client.ExplainaboardClient()

# Dummy data
system_output = [{"predicted_label":"positive"}] * 1821 # the number of test samples


# Do the evaluation
evaluation_result = client.evaluate_system(
    task="text-classification",
    system_name="my-first-system",
    system_output=system_output,
    dataset=sst,
    split="test",
    source_language="en",
    system_details={},
)

# print(evaluation_result)
# print(evaluation_result['system_info']['results']['overall'][0])

```


## Load DataLab Dataset from Files

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
    system_output_file='../../example/data/text_classification/sst2-lstm-output.txt',
    system_output_file_type='text',
    dataset='sst2',
    split='test',
    source_language='en',
)
```