# Command Line Access to ExplainaBoard

You can use `explainaboard_client` to evaluate, browse, and delete systems.

## Evaluation

The most common usage of this client will probably be to
evaluate systems on the ExplainaBoard server. You can do that from the
command line.

If you are using a pre-existing dataset viewable from the
[ExplainaBoard datasets](https://explainaboard.inspiredco.ai/datasets)
page then you can use something like the following command:

```shell
python -m explainaboard_client.cli.evaluate_system \
  --username $EB_USERNAME --api-key $EB_API_KEY \
  --task [TASK_ID] \
  --system-name [MODEL_NAME] \
  --system-output-file [SYSTEM_OUTPUT] --system-output-file-type [FILE_TYPE] \
  --dataset [DATASET] --sub-dataset [SUB_DATASET] --split [SPLIT] \
  --source-language [SOURCE] --target-language [TARGET] \
  [--public]
```

You will need to fill in all the settings appropriately, for example:
* `[TASK_ID]` is the ID of the task you want to perform. A full list is [here](https://github.com/neulab/explainaboard_web/blob/main/backend/src/impl/tasks.py).
* `[MODEL_NAME]` is whatever name you want to give to your model.
* `[SYSTEM_OUTPUT_FILE]` is the file that you want to evaluate. The file format depends
  on the task, and you can see the list of
  [ExplainaBoard task file formats](https://github.com/neulab/ExplainaBoard/blob/main/docs/task_file_formats.md)
  for more details..
* `[FILE_TYPE]` is the type of the file, "text", "tsv", "csv", "conll", or "json".
* `[DATASET]`, `[SUB_DATASET]` and `[SPLIT]` indicate which dataset you're evaluating
  a system output for.
* `[SOURCE]` and `[TARGET]` language indicate the language code of the input and output of
  the system. Please refer to the [ISO-639-3](https://iso639-3.sil.org/code_tables/639/data) list for the 3-character 693-3 language codes. Enter `other-[your custom languages]` if the dataset uses custom languages. Enter `none` if the dataset uses other modalities like images. If the inputs and outputs are the in the same language you only need to
  specify one or the other.
* By default your systems will be private, but if you add the `--public` flag they
  will be made public on the public leaderboards and system listing.

## Evaluation with Custom Datasets

You can also evaluate results for custom datasets
that are not supported by ExplainaBoard yet:

```shell
python -m explainaboard_client.cli.evaluate_system \
  --username $EB_USERNAME --api-key $EB_API_KEY \
  --task [TASK_ID] \
  --system-name [MODEL_NAME] \
  --system-output-file [SYSTEM_OUTPUT] --system-output-file-type [FILE_TYPE] \
  --custom-dataset-file [CUSTOM_DATASET] --custom-dataset-file-type [FILE_TYPE] \
  --source-language [SOURCE] --target-language [TARGET]
```

with similar file and file-type arguments to the system output above. If you're
interested in getting your datasets directly supported within ExplainaBoard, please
open an issue or send a PR to [DataLab](https://github.com/expressai/datalab), and we'll
be happy to help out!

## Finding Uploaded Systems

You can also find systems that have already been evaluated
using the following syntax
```shell
python -m explainaboard_client.cli.find_systems \
  --username $EB_USERNAME --api-key $EB_API_KEY --output-format tsv
```
By default this outputs in a summarized TSV format (similar to the online system
browser), but you can set `--output-format json` to get more extensive information.
There are many options for how you can specify which systems you want to find, which you
can take a look at by running `python -m explainaboard_client.cli.find_systems` without
any arguments.

## Deleting System Outputs

You can delete existing system outputs using the following
command:
```shell
python -m explainaboard_client.cli.delete_systems \
  --username $EB_USERNAME --api-key $EB_API_KEY --system-ids XXX YYY
```
Here the `system_ids` are the unique identifier of each system returned in the
`system_id` field of the JSON returned by the `find_systems` command above. The system
IDs are *not* the system name as displayed in the interface.

## Evaluating Systems on Benchmarks from the Command Line
Instead of simply evaluating an individual system, another common scenario is 
to submit a group of systems to a benchmark (e.g., GLUE). To achieve this goal,
you can follow the command below: 

```shell
python -m explainaboard_client.cli.evaluate_benchmark \
      --username XXX  \
      --api-key YYY \
      --system-name your_system \
      --system-outputs submissions/* \
      --benchmark benchmark_config.json \
      --server local
```
where
* `--username`: the email of your explainaboard account
* `--api-key`: your API key
* `--system-name`: the system name of your submission. Note: this assumes that all
system output share one system name.
* `--benchmark`: the benchmark config file (you can check out this [doc](TBC) to see how to configure the benchmark.)
* `--system-outputs`: system output files. Note that the order of `--system-outputs` files should
strictly correspond to the dataset order of `datasets` in `benchmark_config.json`.
* By default, your systems will be private, but if you add the `--public` flag, they
  will be made public on the public leaderboards and system listing.
  
Here is one [example](./example/benchmark/gaokao/) for the `Gaokao` benchmark.

