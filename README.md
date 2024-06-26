[![Tests passing](https://github.com/CUREd-Plus/curedcolumns/actions/workflows/test.yml/badge.svg)](https://github.com/CUREd-Plus/curedcolumns/actions/workflows/test.yml)

# CUREd+ metadata generator

The CUREd+ metadata generator tool generates a list of all the columns in every table in the database.

# Installation

```bash
pip install curedcolumns
```

# Usage

```bash
curedcolumns --help
```

## Example

Use the [AWS CLI](https://docs.aws.amazon.com/cli/v1/userguide/) profile named "clean"

```bash
curedcolumns --profile clean s3://my_bucket.aws.com
```

# Development

See [CONTRIBUTING.md](./CONTRIBUTING.md).
