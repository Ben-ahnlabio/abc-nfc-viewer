import enum
from typing import List, Optional, TypedDict

import pydantic


class Chain(enum.Enum):
    ETHEREUM = "ethereum"
    KLAYTN = "klaytn"
    POLYGON = "polygon"
    BINANCE = "binance"


class NftAttribute(pydantic.BaseModel):
    trait_type: str
    value: str


class NftUrl(pydantic.BaseModel):
    small: Optional[str]
    large: Optional[str]
    original: str


class NftMetadata(pydantic.BaseModel):
    owner: Optional[str]
    chain: str  # ethereum, klaytn, polygon, binance
    contract_address: str
    token_id: str
    token_type: str
    name: str
    description: Optional[str]
    image: Optional[str]  # token uri 상의 NFT image. (http, IPFS, raw data)
    animation_url: Optional[str]  # opensea 의 video, music nft 의 source url
    url: Optional[NftUrl]
    attributes: Optional[List[NftAttribute]]
    cached: bool = True  # cache 데이터인지 ? API 데이터인지

    def __str__(self) -> str:
        return f"[{self.chain} - {self.token_type}] {self.name} - {self.description}"


class NftResponse(pydantic.BaseModel):
    items: Optional[List[NftMetadata]]


class KlaytnNftContract(pydantic.BaseModel):
    address: str
    name: str
    symbol: str
    logo: str
    total_supply: str
    status: str
    type: str
    created_at: int
    updated_at: int
    deleted_at: int
    cached: bool
