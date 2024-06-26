import logging
from pathlib import Path
from typing import Union

import pyarrow.parquet

logger = logging.getLogger(__name__)


def get_s3_parquet_schema(bucket: str, key: Union[str, Path]) -> pyarrow.Schema:
    """
    List the column names for a table
    """

    uri = f"s3://{bucket}/{key}/*.parquet"

    logger.info(uri)

    # Use pyarrow to access the metadata
    dataset = pyarrow.parquet.ParquetDataset(uri)

    return dataset.schema
