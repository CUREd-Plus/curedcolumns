[![Tests passing](https://github.com/CUREd-Plus/curedcolumns/actions/workflows/test.yml/badge.svg)](https://github.com/CUREd-Plus/curedcolumns/actions/workflows/test.yml)

# CUREd+ metadata generator

The CUREd+ metadata generator tool generates a list of all the columns in every table in the database.

# Installation

Ensure [Python](https://www.python.org/) is installed.

Install [AWS command-line interface (CLI)](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-welcome.html).

Install this package using the [Python package manager](https://pip.pypa.io/en/stable/):

```bash
pip install curedcolumns
```

# Usage

The basic usage of this app is to specify the AWS CLI profile and the bucket name you want to inspect.

```bash
curedcolumns --profile $AWS_PROFILE $AWS_BUCKET
```

You should create an AWS profile using the [`aws configure`](https://docs.aws.amazon.com/cli/v1/userguide/cli-chap-configure.html) command.

```bash
aws configure --profile $AWS_PROFILE
```

To view the command line options:

```bash
$ curedcolumns --help
usage: curedcolumns [-h] [-v] [--version] [-l LOGLEVEL] [--prefix PREFIX] [--no-sign-request] [--profile PROFILE] [-d DELIMITER] bucket

List all the field names for all the data sets in a bucket on AWS S3 object storage and display the metadata in CSV format. This assumes a folder structure in this layout: <data_set_id>/<table_id>/data/*.parquet

positional arguments:
  bucket                S3 bucket location URI

options:
  -h, --help            show this help message and exit
  -v, --verbose
  --version             Show the version number of this tool
  -l LOGLEVEL, --loglevel LOGLEVEL
  --prefix PREFIX       Limits the response to keys that begin with the specified prefix.
  --no-sign-request
  --profile PROFILE     AWS profile to use
  -d DELIMITER, --delimiter DELIMITER
                        Column separator character

```

## Example

Use the [AWS CLI](https://docs.aws.amazon.com/cli/v1/userguide/) profile named "clean"

```bash
curedcolumns --profile clean s3://my_bucket.aws.com
```

# Development

See [CONTRIBUTING.md](https://github.com/CUREd-Plus/curedcolumns/blob/main/CONTRIBUTING.md).
