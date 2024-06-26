import pytest

import curedcolumns


def test_get_s3_parquet_schema(session):
    pytest.skip("Not implemented")
    curedcolumns.get_s3_parquet_schema(session=session, bucket='testing', key='data.parquet')
