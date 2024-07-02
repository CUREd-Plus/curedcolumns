import pyarrow
import pytest

import curedcolumns


def test_get_s3_parquet_schema(session, bucket, key):
    schema = curedcolumns.get_s3_parquet_schema(session=session, bucket=bucket, key=key)

    assert isinstance(schema, pyarrow.Schema)
    assert isinstance(schema.field_by_name('id'), pyarrow.Field)
