# scikit-learn

This is an example of using the ExplainaBoard client with scikit-learn data.

## Example

Here is a somewhat simplified example that abstracts away from the details of model
training. You can see a full example in [main.py](main.py).

```python
import sklearn
import explainaboard_client

# Train a model using scikit-learn and make predictions in your normal way
...
classifier.fit(X_train, y_train)
y_predict = classifier.predict(X_test)

# Create the ExplainaBoard client, wrap the data
explainaboard_client.username = os.environ.get("EB_USERNAME")
explainaboard_client.api_key = os.environ.get("EB_API_KEY")
explainaboard_client.check_api_version = False
client = explainaboard_client.ExplainaboardClient()

# Wrap the data in ExplainaBoard format
dataset_wrapped = explainaboard_client.wrap_tabular_dataset(
    X_test,
    y_test,
    column_names=[...],
    columns_to_analyze=[...],
)
predict_wrapped = explainaboard_client.wrap_tabular_predictions(
    y_predict,
)

# Do the evaluation
evaluation_result = client.evaluate_system(
    task='tabular-classification',
    system_name='iris-test',
    custom_dataset=dataset_wrapped,
    system_output=predict_wrapped,
    split='test',
    source_language='en',
    system_details={},
)

# Print the results
print(f'Successfully submitted system!\n'
      f'Name: {evaluation_result["system_name"]}\n'
      f'ID: {evaluation_result["system_id"]}')
results = evaluation_result['results']['example'].items()
for metric_name, value in results:
    print(f'{metric_name}: {value:.4f}')
```

## Setup

Install the necessary packages

```bash
pip install -r requirements.txt
```
