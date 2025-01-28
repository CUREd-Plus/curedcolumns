#!/usr/bin/env python

import argparse
import csv
import logging
import os
import sys
from pathlib import Path

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
    parser.add_argument('-l', '--loglevel', default='INFO')
    parser.add_argument('bucket', type=bucket_str, help='S3 bucket location URI')
    parser.add_argument('--prefix', required=False, default='',
                        help='Limits the response to keys that begin with the specified prefix.')
    parser.add_argument('--no-sign-request', action='store_true')
    parser.add_argument('--profile', default=AWS_PROFILE, help='AWS profile to use')
    parser.add_argument('-d', '--delimiter', default=',', help='Column separator character')
    parser.add_argument('-o', '--output', type=Path, help='Output file path. Default: screen')
    parser.add_argument('-f', '--force', action='store_true', help='Overwrite output file if it already exists')

    return parser.parse_args()


def main():
    args = get_args()
    logging.basicConfig(
        format="%(name)s:%(asctime)s:%(levelname)s:%(message)s",
        level=logging.DEBUG if args.verbose else args.loglevel
    )

    # Connect to AWS
    # https://boto3.amazonaws.com/v1/documentation/api/latest/guide/session.html
    session: boto3.session.Session = boto3.session.Session(profile_name=args.profile)
    'AWS connection session'
    s3_client = session.client('s3')
    'AWS S3 service client'

    # Store the tables we've already looked at
    tables = set()

    # Select output (write to screen or target file)
    # If a file is selected, open it for writing
    try:
        # Default: open for exclusive creation, failing if the file already exists
        # https://docs.python.org/3/library/functions.html#open
        mode = 'w' if args.force else 'x'
        args.output.parent.mkdir(exist_ok=True, parents=True)
        output = args.output.open(mode)
        logger.info("Writing to '%s'", args.output)
    # if args.output is None
    except AttributeError:
        # Default: Write to screen
        output = sys.stdout
    except FileExistsError:
        logger.warning("Output file '%s' already exists", args.output)
        logger.info("Use --force to overwrite")
        exit()

    # Output to CSV format
    writer = csv.DictWriter(output, fieldnames=HEADERS)
    # Show CSV header
    writer.writeheader()

    # Iterate over all files
    for path in curedcolumns.iter_files(s3_client, args.bucket, prefix=args.prefix):
        # Parse the path structure
        # It should be /<data_set_id>/<table_id>/data/**/*.parquet
        relative_path = path.relative_to(args.prefix)
        data_set_id, table_id = relative_path.parts[0:2]

        # Skip other files such as appendix ones
        if relative_path.parts[2] != 'data':
            logger.warning("Skipping: %s", relative_path)
            continue

        full_table_id = (data_set_id, table_id)
        # Keep track of the ones we've already looked at
        if full_table_id in tables:
            # If we already processed this, then skip to the next file
            continue
        else:
            tables.add(full_table_id)

        logger.info("Table: %s.%s", data_set_id, table_id)

        # Get column names
        key = Path(data_set_id) / table_id / "data"
        schema = curedcolumns.get_s3_parquet_schema(bucket=args.bucket, key=key, session=session)
        for column in schema:
            row = dict(
                data_set_id=data_set_id,
                table_id=table_id,
                column_name=column.name,
                data_type=column.type
            )
            writer.writerow(row)

    # Tell the user that the output file was written
    if args.output:
        logger.info("Wrote '%s'", args.output)


if __name__ == '__main__':
    main()
