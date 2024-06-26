import pyarrow.parquet


def get_s3_parquet_schema(bucket: str, key: str) -> pyarrow.Schema:
    """
    List the column names for a table
    """

    uri = f"s3://{bucket}/{key}"

    # Use pyarrow to access the metadata
    dataset = pyarrow.parquet.ParquetDataset(uri)

    return dataset.schema
