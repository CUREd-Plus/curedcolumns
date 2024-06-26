"""
https://docs.getmoto.org/en/latest/docs/getting_started.html#recommended-usage
"""

import os

import boto3
import moto
import pytest


@pytest.fixture(scope="function")
def aws_credentials():
    """
    Mocked AWS Credentials for moto.
    """
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def s3_client(session):
    """
    Mock AWS S3 Client
    """

    with moto.mock_aws():
        yield session.client('s3')


@pytest.fixture(scope="function")
def session(aws_credentials):
    """
    Mock AWS session
    """
    with moto.mock_aws():
        yield boto3.Session()
