from anv import repository


def test_s3_source_repository(
    s3_src_repo: repository.AWSS3SourceRepository,
):
    uri = "https://metadata.ens.domains/mainnet/0x57f1887a8bf19b14fc0df6fd9b2acc9af147ea85/0x9578c76bd50e7f24a7a52424a94950d6ff2f1d986320d645b1390ad0a5c6f89c/image"
    url_source = s3_src_repo._cache_uri_source(uri)
    assert url_source
