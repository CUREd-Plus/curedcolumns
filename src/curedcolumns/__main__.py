#!/usr/bin/env python

import argparse
import csv
import logging
import os
import pathlib
import sys

import boto3

import curedcolumns
from curedcolumns.exceptions import CuredFileNotFoundError

DESCRIPTION = """
List all the field names for all the data sets in a bucket on AWS S3 object storage and display the metadata in CSV
format.

This assumes a folder structure in this layout:
<data_set_id>/<table_id>/data/*.parquet
"""

logger = logging.getLogger(__name__)

AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')

HEADERS = ('data_set_id', 'table_id', 'column_name', 'data_type')


def bucket_str(bucket: str) -> str:
    """
    Remove URL prefix from the bucket name string
    """
    return bucket.lstrip('s3://')


def get_args() -> argparse.Namespace:
    """
    Set up command-line arguments
    """

    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('--version', action='version', version='%(prog)s ' + curedcolumns.__version__,
                        help='Show the version number of this tool')
    parser.add_argument('-l', '--loglevel', default='WARNING')
    parser.add_argument('bucket', type=bucket_str, help='S3 bucket location URI')
    parser.add_argument('--prefix', required=False, default='',
                        help='Limits the response to keys that begin with the specified prefix.')
    parser.add_argument('--no-sign-request', action='store_true')
    parser.add_argument('--profile', default=AWS_PROFILE, help='AWS profile to use')
    parser.add_argument('-d', '--delimiter', default=',', help='Column separator character')
    parser.add_argument('-o', '--output', type=pathlib.Path, help='Output file path. Default: screen')

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

    # Select output (write to screen or target file)
    output = sys.stdout
    # If a file is selected, open it for writing
    try:
        output = args.output.open('a')
    except AttributeError:
        pass

    # Output to CSV format
    writer = csv.DictWriter(output, fieldnames=HEADERS)
    # Show CSV header
    writer.writeheader()

    # Iterate over all files
    for path in curedcolumns.iter_files(s3_client, args.bucket, prefix=args.prefix):
        # Parse the path structure
        # It should be /<data_set_id>/<table_id>/data/*.parquet
        data_set_id, table_id = path.relative_to(args.prefix).parts[0:2]

        # Check the directory structure is correct
        try:
            if 'data' in {data_set_id, table_id}:
                raise CuredFileNotFoundError(path)
            data_path = path.parent
            if data_path.name != 'data':
                raise CuredFileNotFoundError(path)
        except CuredFileNotFoundError:
            # Describe the problem
            logger.error("The data set or table does not exist at %s", path)
            logger.warning("Expecting: ./<data_set_id>/<table_id>/data/*.parquet")
            exit()

        # Keep track of the ones we've already looked at
        if data_path in data_paths:
            # If we already processed this, then skip to the next file
            continue
        else:
            data_paths.add(data_path)

        logger.info("Data set ID: %s\tTable ID %s", data_set_id, table_id)

        # Get column names
        schema = curedcolumns.get_s3_parquet_schema(bucket=args.bucket, key=data_path, session=session)
        for column in schema:
            row = dict(
                data_set_id=data_set_id,
                table_id=table_id,
                column_name=column.name,
                data_type=column.type
            )
            writer.writerow(row)


if __name__ == '__main__':
    main()
