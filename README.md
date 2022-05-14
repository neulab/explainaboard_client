# ExplainaBoard CLI

## Install
- For CLI users
    - `pip install explainaboard_cli`
- For CLI developers
    - `pip install .`

## Update

There are two packages associated with this CLI: `explainaboard_api_client` and `explainaboard_cli`
- `explainaboard_api_client`: auto generated according to OpenAPI definition specified in [openapi.yaml](https://github.com/neulab/explainaboard_web/tree/main/openapi). Version of this client is specified in the same yaml file (`info.version`).
  - To update: `pip install -U explainaboard_api_client` or specify a specific version
  - To check the API version used in the live environment: `curl https://explainaboard.inspiredco.ai/api/info` (this information will be added to the UI in the future)
- `explainaboard_cli`: a thin wrapper for the API client to make it easy to use. It helps users configure API keys, choose host names, load files from local FS, etc. Usually, this package is relatively stable so you don't need to update unless a new feature of the CLI is released.
  - To update: `pip install -U explainaboard_cli`



Please see examples in `./tests`