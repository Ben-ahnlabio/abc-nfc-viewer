import os
from typing import IO, Any, Dict, Optional, Union
import boto3
import mypy_boto3_s3
from mypy_boto3_s3 import type_defs
from botocore.response import StreamingBody


class AWSS3Storage:
    def __init__(self):
        self.region_name = os.environ["AWS_S3_REGION_NAME"]
        self.bucket_name = os.environ["AWS_S3_BUCKET_NAME"]
        self.s3: mypy_boto3_s3.S3Client = boto3.client(
            service_name="s3",
            region_name=self.region_name,
            aws_access_key_id=os.environ["AWS_S3_ACCESS_KEY"],
            aws_secret_access_key=os.environ["AWS_S3_SECRET_KEY"],
        )
        self.base_url = (
            f"https://{self.bucket_name}.s3.{self.region_name}.amazonaws.com/"
        )
        self.resize_base_url = (
            f"https://{self.bucket_name}-resized.s3.{self.region_name}.amazonaws.com/"
        )

    def upload_object(
        self,
        file_obj: Union[IO[Any], StreamingBody],
        key: str,
        extra_args: Dict[str, Any],
    ):
        self.s3.upload_fileobj(
            Fileobj=file_obj, Bucket=self.bucket_name, Key=key, ExtraArgs=extra_args
        )

    def find_first_object(self, prefix: str) -> Optional[type_defs.ObjectTypeDef]:
        objs = self.list_object(prefix)
        contents = objs.get("Contents", [])
        try:
            return contents[0]
        except IndexError:
            return None

    def get_object(self, key: str):
        return self.s3.get_object(Bucket=self.bucket_name, Key=key)

    def list_object(self, prefix: str):
        return self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)

    def remove_object(self, key: str):
        return self.s3.delete_object(Bucket=self.bucket_name, Key=key)
