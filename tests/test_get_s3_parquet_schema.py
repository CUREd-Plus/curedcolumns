import moto
import pyarrow
import pytest

import curedcolumns


@moto.mock_aws
def test_get_s3_parquet_schema(session, bucket, keys):
    pytest.skip("This test doesn't work yet")

    for key in keys:
        schema = curedcolumns.get_s3_parquet_schema(session=session, bucket=bucket, key=key)

        assert isinstance(schema, pyarrow.Schema)
        assert isinstance(schema.field_by_name('id'), pyarrow.Field)
