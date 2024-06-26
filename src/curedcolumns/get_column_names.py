import pyarrow.parquet


def get_parquet_column_names(bucket: str, key: str):
    """
    List the column names for a table
    """

    # Use pyarrow to access the ParquetDataset
    dataset = pyarrow.parquet.ParquetDataset(f"s3://{bucket}/{key}")

    # Get column names from schema
    return dataset.schema.names
