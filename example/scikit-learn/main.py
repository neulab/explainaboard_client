import os

import explainaboard_client
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

url = "iris.csv"
dataset = pd.read_csv(url)
names = dataset.columns.values.tolist()
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, 4].values
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.50)

# Run the classifier
classifier = KNeighborsClassifier(n_neighbors=5)
classifier.fit(X_train, y_train)
y_predict = classifier.predict(X_test)

# Create the ExplainaBoard client, wrap the data, and evaluate
explainaboard_client.username = os.environ.get("EB_USERNAME")
explainaboard_client.api_key = os.environ.get("EB_API_KEY")
client = explainaboard_client.ExplainaboardClient()

dataset_wrapped = explainaboard_client.wrap_tabular_dataset(
    X_test,
    y_test,
    column_names=names[:-1],
    columns_to_analyze=["sepal.length", "sepal.width", "petal.length", "petal.width"],
)
predict_wrapped = explainaboard_client.wrap_tabular_predictions(
    y_predict,
)

# Do the evaluation
evaluation_result = client.evaluate_system(
    task="tabular-classification",
    system_name="iris-test",
    custom_dataset=dataset_wrapped,
    system_output=predict_wrapped,
    split="test",
    source_language="en",
    system_details={},
)

# Print the results
print(
    f"Successfully submitted system!\n"
    f'Name: {evaluation_result["system_name"]}\n'
    f'ID: {evaluation_result["system_id"]}'
)
results = evaluation_result["results"]["example"].items()
for metric_name, value in results:
    print(f"{metric_name}: {value:.4f}")
