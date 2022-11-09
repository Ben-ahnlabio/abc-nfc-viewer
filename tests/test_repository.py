from anv import repository, models
from anv.api import alchemy


def test_disk_repository(alchemy_api: alchemy.AlchemyApi):
    data = {
        "contract_address": "0x2931b181ae9dc8f8109ec41c42480933f411ef94",
        "token_id": "0x0000000000000000000000000000000000000000000000000000000000000262",
        "token_type": "ERC721",
        "name": "SlimHood #610",
        "description": "They all wear hoods, but each SlimHood is unique.",
        "image": "ipfs://QmPCzRHRgCdPrhNnfG9tPvM5jp18TmoJwBrfkgcyFipe7b/610.gif",
        "url": None,
        "attributes": [
            {"trait_type": "Hoodie", "value": "Orange/Red/White/Green"},
            {"trait_type": "Hood", "value": "Hood Down"},
            {"trait_type": "Pants", "value": "Orange Sweatpants"},
            {"trait_type": "Footwear", "value": "Black Boots"},
            {"trait_type": "Hat", "value": "Green Beanie"},
            {"trait_type": "Headphones", "value": "No Headphones"},
            {"trait_type": "Skin", "value": "Skin 3"},
            {"trait_type": "Hair", "value": "Light Brown Short Hair"},
            {"trait_type": "Beard", "value": "No Beard"},
            {"trait_type": "Mouth", "value": "Kissing Mouth"},
            {"trait_type": "Eyes", "value": "Black Shades"},
        ],
        "cached": True,
    }
    repo = repository.DiskRepository()

    contract_address = "0x2931b181ae9dc8f8109ec41c42480933f411ef94"
    token_id = "0x0000000000000000000000000000000000000000000000000000000000000262"

    metadata = models.NftMetadata.parse_obj(data)
    result = repo.set_NFT_metadata(models.Network.ETHEREUM, metadata)
    assert result

    cached_metadata = repo.get_NFT_metadata(
        models.Network.ETHEREUM, contract_address, token_id
    )
    assert cached_metadata
    assert metadata == cached_metadata
