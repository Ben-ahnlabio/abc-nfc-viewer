import os
from anv import repository, models

os.environ["MONGODB_HOST"] = "cluster0.gpvm5.gcp.mongodb.net"
os.environ["MONGODB_USER"] = "ricepotato"
os.environ["MONGODB_PASSWORD"] = "qkqhshadk40"


def test_get_mongodb_nft_metadata_repo():
    metadata = {
        "owner": None,
        "chain": "ethereum",
        "contract_address": "0x495f947276749ce646f68ac8c248420045cb7b5e",
        "token_id": "0x706b288c30b6659c3d0ec5aefac9a7017a1dae9d000000000000d50000000001",
        "token_type": "ERC1155",
        "name": "MVP #189",
        "description": None,
        "image": "https://lh3.googleusercontent.com/YPIfpyaD-TMHctOt0lj7XTLtdrikr0tf7rUibXmVazFmAg5KlqovweL_Zre4aO4wIe5qhmwRtH499b-XPmVXnQw3-ymjhnlYLCKB0Hk",
        "animation_url": None,
        "url": None,
        "attributes": [],
        "cached": False,
    }
    repo = repository.MongodbRepository()
    metadata_obj = models.NftMetadata.parse_obj(metadata)
    result = repo.set_NFT_metadata(metadata_obj)
    assert result

    result = repo.get_NFT_metadata(
        models.Chain.ETHEREUM, metadata_obj.contract_address, metadata_obj.token_id
    )
    assert result
