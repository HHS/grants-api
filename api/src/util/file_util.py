import os
from pathlib import PosixPath
from typing import Any, Optional, Tuple
from urllib.parse import urlparse

import smart_open
from botocore.config import Config

from src.adapters.aws import S3Config, get_boto_session, get_s3_client

##################################
# Path parsing utils
##################################


def is_s3_path(path: str | PosixPath) -> bool:
    return str(path).startswith("s3://")


def split_s3_url(path: str) -> Tuple[str, str]:
    parts = urlparse(path)
    bucket_name = parts.netloc
    prefix = parts.path.lstrip("/")
    return (bucket_name, prefix)


def get_s3_bucket(path: str) -> Optional[str]:
    return urlparse(path).hostname


def get_s3_file_key(path: str) -> str:
    return urlparse(path).path[1:]


def get_file_name(path: str) -> str:
    return os.path.basename(path)


def join(*parts: str) -> str:
    return os.path.join(*parts)


##################################
#  File operations
##################################


def open_stream(path: str, mode: str = "r", encoding: str | None = None) -> Any:
    if is_s3_path(path):
        so_config = Config(
            max_pool_connections=10,
            connect_timeout=60,
            read_timeout=60,
            retries={"max_attempts": 10},
        )
        so_transport_params = {"client_kwargs": {"config": so_config}}

        return smart_open.open(path, mode, transport_params=so_transport_params, encoding=encoding)
    else:
        return smart_open.open(path, mode, encoding=encoding)


def pre_sign_file_location(file_path: str) -> str:
    s3_config = S3Config()
    s3_client = get_s3_client(s3_config, get_boto_session())
    bucket, key = split_s3_url(file_path)
    pre_sign_file_loc = s3_client.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket, "Key": key},
        ExpiresIn=s3_config.presigned_s3_duration,
    )
    if s3_config.s3_endpoint_url:
        # Only relevant when local, due to docker path issues
        pre_sign_file_loc = pre_sign_file_loc.replace(
            s3_config.s3_endpoint_url, "http://localhost:4566"
        )

    return pre_sign_file_loc


def get_file_length_bytes(path: str) -> int:
    if is_s3_path(path):
        s3_client = (
            get_s3_client()
        )  # from our aws utils - handles some of the weird localstack stuff

        bucket, key = split_s3_url(path)
        file_metadata = s3_client.head_object(Bucket=bucket, Key=key)
        return file_metadata["ContentLength"]

    file_stats = os.stat(path)
    return file_stats.st_size


def delete_file(path: str) -> None:
    """Delete a file from s3 or local disk"""
    if is_s3_path(path):
        bucket, s3_path = split_s3_url(path)

        s3_client = get_s3_client()
        s3_client.delete_object(Bucket=bucket, Key=s3_path)
    else:
        os.remove(path)
