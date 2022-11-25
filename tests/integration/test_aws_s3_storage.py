import pathlib
import tempfile
from anv import aws_s3


def test_aws_s3_storage_create(aws_s3_obj: aws_s3.AWSS3Storage):
    pass


def test_aws_s3_storage_upload_file_obj(aws_s3_obj: aws_s3.AWSS3Storage):
    key = "abc_test_file.txt"
    # arn:aws:s3:::abc-nft-source
    with tempfile.TemporaryDirectory() as dir:
        tmp_file = pathlib.Path(dir) / key
        with tmp_file.open("w") as f:
            f.write("tmp file content")

        with tmp_file.open("rb") as f:
            aws_s3_obj.upload_object(f, key, {"ContentType": "text/plain"})

    obj = aws_s3_obj.find_first_object("ccd")
    assert obj is None

    obj = aws_s3_obj.find_first_object("abc_test")
    assert obj
    result = aws_s3_obj.remove_object(obj["Key"])
    assert result
