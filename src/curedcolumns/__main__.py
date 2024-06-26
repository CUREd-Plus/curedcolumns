#!/usr/bin/env python

import argparse
import logging
import os
import pathlib

import boto3

from curedcolumns.iter_files import iter_files
from curedcolumns.get_parquet_column_names import get_s3_parquet_schema

DESCRIPTION = """
List all the field names for all the data sets in a bucket on AWS S3 object storage.

This assumes a folder structure in this layout:
<data_set_id>/<table_id>/data/*.parquet
"""

logger = logging.getLogger(__name__)

AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')


def bucket_str(bucket: str) -> str:
    """
    Remove URL prefix from the bucket name string
    """
    return bucket.lstrip('s3://')


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--loglevel', default='WARNING')
    parser.add_argument('bucket', type=bucket_str, help='S3 bucket location URI')
    parser.add_argument('--prefix', required=False, default='',
                        help='Limits the response to keys that begin with the specified prefix.')
    parser.add_argument('--no-sign-request', action='store_true')
    parser.add_argument('--profile', default=AWS_PROFILE, help='AWS profile to use')
    return parser.parse_args()


def main():
    args = get_args()
    logging.basicConfig(
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s",
        level=logging.INFO if args.verbose else args.loglevel
    )

    # Connect to AWS
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    session: boto3.session.Session = boto3.session.Session(profile_name=args.profile)
    'AWS connection session'
    s3_client = session.client('s3')
    'AWS S3 service client'

    # Store the data directories we've already looked at
    data_paths: set[pathlib.Path] = set()

    # Iterate over all files
    for path in iter_files(s3_client, args.bucket, prefix=args.prefix):
        logger.info(path)
        data_set_id, table_id = path.relative_to(args.prefix).parts[0:2]
        logger.info("Data set ID: %s\ttable ID %s", data_set_id, table_id)

        # Get path of table data
        # This assumes that the parquet files are in a d
        data_path = path.parent
        if data_path.name != 'data':
            raise ValueError(path)

        # If we already processed this, then skip to the next file
        if data_path in data_paths:
            continue

        data_paths.add(data_path)

        # Get column names
        for schema in get_s3_parquet_schema(bucket=args.bucket, key=data_path, session=session):
            print(schema)


if __name__ == '__main__':
    main()
