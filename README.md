# ExplainaBoard Client

This is a command line and API client that makes it easy for you to evaluate systems
using [ExplainaBoard](https://explainaboard.inspiredco.ai).

## Preparation

**Install:** First, install the client.

```bash
pip install explainaboard_client
```

**Acquiring a Login and API Key:**
Create an account at the [ExplainaBoard](https://explainaboard.inspiredco.ai)
site and log in. Once you are logged in, you can click on
the upper-right corner of the screen, and it will display your email and API key, which 
you can copy-paste.

You can save these into environmental variables for convenient use in the commands
below:

```
export EB_USERNAME="[your username]"
export EB_API_KEY="[your API key]"
```

## Use in Python

The most common usage of this client will probably be to
evaluate systems on the ExplainaBoard server.
Below is an example of how you can do this in Python.

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

For more details on precisely how to specify all the variables, as well as how to do
other things such as search for and delete systems, see the
[documentation of the Python API](docs/python_api/introduction.md).

## Use from the Command Line

You can also evaluate systems from the command line like this.

```shell
python -m explainaboard_client.cli.evaluate_system \
  --task text-classification \
  --system-name text-classification-test \
  --system-output-file example/data/sst2-lstm-output.txt \
  --system-output-file-type text \
  --dataset sst2 \
  --split test \
  --source-language 'en'
```

For more details, see the [command line documentation](docs/cli.md).

## Having Trouble?

Please [open an issue](https://github.com/neulab/explainaboard_client/issues) on the
issues page and we'll be happy to help!