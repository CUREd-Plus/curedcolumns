import logging
from pathlib import Path
from typing import Union

import pyarrow.fs
import pyarrow.parquet

logger = logging.getLogger(__name__)


def get_s3_parquet_schema(session, bucket: str, key: Union[str, Path]) -> pyarrow.Schema:
    """
    List the column names for a table
    """

    uri = f"s3://{bucket}/{key}/*.parquet"

    file_system = pyarrow.fs.S3FileSystem(session=session)

    logger.info(uri)

    # Use pyarrow to access the metadata
    data_set = pyarrow.parquet.ParquetDataset(uri, filesystem=file_system)

    return data_set.schema
