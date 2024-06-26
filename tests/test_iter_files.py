import pytest

import curedcolumns


def test_iter_files(s3_client):
    curedcolumns.iter_files(s3_client=s3_client, bucket='test-bucket')
