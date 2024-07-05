"""
Testing with Moto (mock AWS for boto3)
https://docs.getmoto.org/en/latest/docs/getting_started.html#recommended-usage
"""
import io
import logging
import os
import random
import string

import boto3
import moto
import numpy
import pyarrow.parquet
import pytest

CREDENTIALS = dict(
    AWS_ACCESS_KEY_ID="testing",
    AWS_SECRET_ACCESS_KEY="testing",
    AWS_SECURITY_TOKEN="testing",
    AWS_SESSION_TOKEN="testing",
    AWS_DEFAULT_REGION="eu-west-2",
)

BUCKET = "test-bucket"
FILENAMES = {'partition_1.parquet', 'partition_2.parquet', 'partition_3.parquet'}

logger = logging.getLogger(__name__)


@pytest.fixture
def aws_credentials():
    """
    Mocked AWS Credentials for moto.
    """

    os.environ.update(CREDENTIALS)


@pytest.fixture
def session(aws_credentials):
    """
    Mock AWS session
    """
    with moto.mock_aws():
        yield boto3.Session()


@pytest.fixture
def s3_client(session):
    """
    Mock AWS S3 Client
    """

    yield session.client('s3')


def generate_table(num_rows: int = 100) -> pyarrow.Table:
    """
    Generate a synthetic data table.
    """

    schema = pyarrow.schema([
        pyarrow.field("id", pyarrow.int64()),
        pyarrow.field("name", pyarrow.string()),
        pyarrow.field("age", pyarrow.int32()),
    ])

    data = dict(
        id=numpy.random.randint(1, 1000, size=num_rows),
        name=["".join(random.choices(string.ascii_letters, k=10)) for _ in range(num_rows)],
        age=numpy.random.randint(18, 65, size=num_rows),
    )

    return pyarrow.Table.from_pydict(data, schema=schema)


@pytest.fixture
def bucket(s3_client):
    """
    Create a test bucket with test data.
    """

    # Create dummy bucket
    response = s3_client.create_bucket(
        Bucket=BUCKET,
        CreateBucketConfiguration={
            'LocationConstraint': CREDENTIALS['AWS_DEFAULT_REGION']}
    )
    logger.debug(response)

    yield BUCKET


@pytest.fixture
def keys(s3_client, bucket):
    """
    Create dummy files on AWS S3.
    """
    keys_: set[str] = set()

    # Generate synthetic data
    table = generate_table()
    buffer = io.BytesIO()
    with pyarrow.parquet.ParquetWriter(buffer, table.schema) as writer:
        writer.write_table(table)
    buffer.seek(0)

    for file_name in FILENAMES:
        # Create S3 blob
        key = f"hes_apc/hes_apc/data/{file_name}"
        response = s3_client.put_object(Bucket=bucket, Body=buffer.getvalue(), Key=key)
        buffer.seek(0)
        logger.debug(response)

        keys_.add(key)

    yield keys_
