import logging
from typing import Generator

logger = logging.getLogger(__name__)


def list_parquet_files(s3_client, bucket: str, prefix: str = None) -> Generator[str, None, None]:
    """
    This function yields the S3 key (path) of parquet files in an S3 bucket as a generator.

    Args:
        s3_client: AWS S3 service client
        bucket: The name of the S3 bucket to search (str).
        prefix: Folder

    Yields:
        The S3 key (path) of each parquet file found (str).
    """
    paginator = s3_client.get_paginator("list_objects_v2")

    logger.info("%s/%s", bucket, prefix)

    # Iterate over pages
    for page in paginator.paginate(Bucket=bucket, Prefix=prefix):

        # Loop through S3 objects (files)
        for obj in page.get("Contents", []):
            s3_key: str = obj["Key"]
            if s3_key.endswith(".parquet"):
                yield s3_key
