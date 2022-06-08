# Instruction of Submitting Systems for Benchmark

This document details how to submit your systems to Gaokao Benchmark 

## Data Preparation
There are two types of files required to make a submission.

* Benchmark config file: `config_gaokao.json` is a config file for Gaokao benchmark that determines
how such a benchmark is composed of a series of datasets. 

* System outputs: `submissions` denotes a folder that contains output files from different 
datasets of this benchmark.


## Command

```shell
python -m explainaboard_client.upload_benchmark \
      --email XXX  \
      --api_key YYY \
      --system_name my_system \
      --system_outputs submissions/* \
      --benchmark config_gaokao.json \
      --server local
```
where
* `--email`: the email of your explainaboard account
* `--api_key`: your API key
* `--system_name`: the system name of your submission. Note: this assumes that all
system output share one system name.
* `--benchmark`: the benchmark config file
* `system_outputs`: system output files. Note that the order of `system_outputs` files should
strictly correspond to the dataset order of `datasets` in `config_gaokao.json`.
* By default, your systems will be private, but if you add the `--public` flag, they
  will be made public on the public leaderboards and system listing.
