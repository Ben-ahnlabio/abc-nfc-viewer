import io
import os
import mimetypes
import pathlib
import tempfile

import boto3
import botocore
import magic
import mypy_boto3_s3
import pytest


def test_aws_file_upload_s3(env_from_file):
    bucket_name = "abc-nft-source"
    image_filepath = "/mnt/c/Users/ben/Downloads/nft_original.jpg"
    s3: mypy_boto3_s3.S3Client = boto3.client(
        service_name="s3",
        region_name=os.getenv("AWS_S3_REGION_NAME"),
        aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_S3_SECRET_KEY"),
    )

    content_type, _ = mimetypes.guess_type(image_filepath)

    key = "nft_abc_test_file"

    s3.delete_object(Bucket=bucket_name, Key=key)
    with pytest.raises(botocore.exceptions.ClientError):
        s3.get_object(Bucket=bucket_name, Key="nft_original2.jpg")

    s3.upload_file(
        Filename=image_filepath,
        Bucket=bucket_name,
        Key=key,
        ExtraArgs={"ContentType": content_type},
    )

    obj = s3.get_object(Bucket=bucket_name, Key=key)
    content_type = obj["ResponseMetadata"]["HTTPHeaders"]["content-type"]
    #
    assert content_type == "image/jpeg"

    with tempfile.TemporaryDirectory() as dir:
        tmp_filepath = pathlib.Path(dir) / "filename"
        s3.download_file(Bucket=bucket_name, Key=key, Filename=str(tmp_filepath))

        content_type, _ = mimetypes.guess_type(tmp_filepath)
        assert content_type == "image/jpeg"


def test_aws_file_obj_upload_s3(env_from_file):
    bucket_name = "abc-nft-source"
    image_filepath = "/mnt/c/Users/ben/Downloads/nft_original.jpg"
    s3: mypy_boto3_s3.S3Client = boto3.client(
        service_name="s3",
        region_name=os.getenv("AWS_S3_REGION_NAME"),
        aws_access_key_id=os.getenv("AWS_S3_ACCESS_KEY"),
        aws_secret_access_key=os.getenv("AWS_S3_SECRET_KEY"),
    )

    content_type, _ = mimetypes.guess_type(image_filepath)
    assert content_type == "image/jpeg"
    key = "0588a0182ee72f74d0b"

    s3.delete_object(Bucket=bucket_name, Key=key)

    with open(image_filepath, "rb") as f:
        with io.BytesIO() as buffer:
            buffer.write(f.read())
            buffer.seek(0)
            content_type = magic.from_buffer(buffer.read(), mime=True)
            buffer.seek(0)
            # s3.upload_fileobj(
            #     Fileobj=buffer,
            #     Bucket=bucket_name,
            #     Key=key,
            #     ExtraArgs={"ContentType": content_type},
            # )
            s3.put_object(
                Bucket=bucket_name, Key=key, Body=buffer, ContentType=content_type
            )

    objs = s3.list_objects_v2(Bucket=bucket_name, Prefix="0588a0c182")
    assert objs

    obj = s3.get_object(Bucket=bucket_name, Key=key)
    content_type = obj["ResponseMetadata"]["HTTPHeaders"]["content-type"]
    assert content_type == "image/jpeg"
    # s3.delete_object(Bucket=bucket_name, Key=key)

    with tempfile.TemporaryDirectory() as dir:
        tmp_filepath = pathlib.Path(dir) / "filename"
        s3.download_file(Bucket=bucket_name, Key=key, Filename=str(tmp_filepath))

        content_type, _ = mimetypes.guess_type(tmp_filepath)
        assert content_type == "image/jpeg"
