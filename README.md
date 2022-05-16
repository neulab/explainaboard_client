# ExplainaBoard Client

This is a command line and API client that makes it easy for you to upload systems to
[ExplainaBoard](https://explainaboard.inspiredco.ai).

## Preparation

### Install

- For CLI/api users
    - `pip install explainaboard_client`
- For explainaboard client developers
    - `pip install .`

### Acquiring a Login and API Key

First, create an account at the [ExplainaBoard](https://explainaboard.inspiredco.ai)
site and remember the email address you used. Once you are logged in, you can click on
the upper-right corner of the screen, and it will display your API key, which you can
copy-paste.

You can save these into environmental variables for convenient use in the commands
below:

```
export EB_EMAIL="[your email]"
export EB_API_KEY="[your API key]"
```

## Usage

### Uploading Systems from the Command Line

The most common usage of this API will probably be to upload systems. You can do that
from the command line. If you are using a pre-existing dataset viewable from the
[ExplainaBoard datasets](https://explainaboard.inspiredco.ai/datasets) page then
you can use something like the following command:

```
python -m explainaboard_client.upload_system \
  --email $EB_EMAIL --api_key $EB_API_KEY \
  --task [TASK_ID] \
  --system_name [MODEL_NAME] \
  --system_output [SYSTEM_OUTPUT] --output_file_type [FILE_TYPE] \
  --dataset [DATASET] --sub_dataset [SUB_DATASET] --split [SPLIT] \
  --source_language [SOURCE] --target_language [TARGET] \
  [--public]
```

You will need to fill in all the settings appropriately, for example:
* `[TASK_ID]` is the ID of the task you want to perform. A full list is [here](https://github.com/neulab/explainaboard_client/blob/main/docs/tasks.py).
* `[MODEL_NAME]` is whatever name you want to give to your model.
* `[SYSTEM_OUTPUT]` is the file that you want to upload.
* `[FILE_TYPE]` is the type of the file, "text", "tsv", "csv", "conll", or "json".
* `[DATASET]`, `[SUB_DATASET]` and `[SPLIT]` indicate which dataset you're uploading
  a system output for.
* `[SOURCE]` and `[TARGET]` language indicate the language of the input and output of
  the system. If the inputs and outputs are the in the same language you only need to
  specify one or the other.
* By default your systems will be private, but if you add the `--public` flag they
  will be made public on the public leaderboards and system listing.

You can also upload for custom datasets that are not supported by ExplainaBoard yet:

```
python -m explainaboard_client.upload_system \
  --email $EB_EMAIL --api_key $EB_API_KEY \
  --task [TASK_ID] \
  --system_name [MODEL_NAME] \
  --system_output [SYSTEM_OUTPUT] --output_file_type [FILE_TYPE] \
  --custom_dataset [CUSTOM_DATASET] --custom_dataset_file_type [FILE_TYPE] \
  --source_language [SOURCE] --target_language [TARGET]
```

with similar file and file-type arguments to the system output above. If you're
interested in getting your datasets directly supported within ExplainaBoard, please
open an issue or send a PR to [DataLab](https://github.com/expressai/datalab), and we'll
be happy to help out!

### Programmatic Usage

Please see examples in `./tests`.
We will be working on more examples and documentation shortly.

## Update

There are two packages associated with this CLI: `explainaboard_api_client` and `explainaboard_client`
- `explainaboard_api_client`: auto generated according to OpenAPI definition specified in [openapi.yaml](https://github.com/neulab/explainaboard_web/tree/main/openapi). Version of this client is specified in the same yaml file (`info.version`).
  - To update: `pip install -U explainaboard_api_client` or specify a specific version
  - To check the API version used in the live environment: `curl https://explainaboard.inspiredco.ai/api/info` (this information will be added to the UI in the future)
- `explainaboard_client`: a thin wrapper for the API client to make it easy to use. It helps users configure API keys, choose host names, load files from local FS, etc. Usually, this package is relatively stable so you don't need to update unless a new feature of the CLI is released.
  - To update: `pip install -U explainaboard_client`



