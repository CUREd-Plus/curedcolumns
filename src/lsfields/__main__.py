#!/usr/bin/env python

import argparse
import logging
import os

import boto3

from lsfields.list_parquet_files import list_parquet_files

DESCRIPTION = """
This will list all the field names for all the data sets
in a bucket on AWS S3 object storage.
"""

logger = logging.getLogger(__name__)

AWS_PROFILE = os.getenv('AWS_PROFILE', 'default')


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=DESCRIPTION)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-l', '--loglevel', default='WARNING')
    parser.add_argument('bucket', help='S3 bucket location URI')
    parser.add_argument('--prefix', required=False, default='')
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

    for file in list_parquet_files(s3_client, args.bucket, prefix=args.prefix):
        print(file)


if __name__ == '__main__':
    main()