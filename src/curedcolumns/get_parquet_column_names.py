import logging
from pathlib import Path
from typing import Union

import pyarrow.fs
import pyarrow.parquet

logger = logging.getLogger(__name__)


def get_s3_parquet_schema(session, bucket: str, key: Union[str, Path]) -> pyarrow.Schema:
    """
    List the column names for a table

    Working with Schema
    https://arrow.apache.org/cookbook/py/schema.html

    :returns: PyArrow table schema
    """

    # Connect to AWS S3
    # https://arrow.apache.org/docs/python/filesystems.html#s3
    credentials = session.get_credentials()
    file_system = pyarrow.fs.S3FileSystem(
        access_key=credentials.access_key,
        secret_key=credentials.secret_key,
        region=session.region_name,
        session_token=credentials.token
    )

    # Build data set location
    uri = f"{bucket}/{key}/*.parquet"
    logger.info(uri)

    # Use pyarrow to access the metadata
    # https://arrow.apache.org/docs/python/parquet.html#
    data_set = pyarrow.parquet.ParquetDataset(uri, filesystem=file_system)

    # https://arrow.apache.org/cookbook/py/schema.html
    return data_set.schema
