import enum
from typing import List, Optional

import pydantic


class Chain(enum.Enum):
    ETHEREUM = "ethereum"
    KLAYTN = "klaytn"
    POLYGON = "polygon"
    BINANCE = "binance"


class NftAttribute(pydantic.BaseModel):
    display_type: Optional[str]
    trait_type: str
    value: str


class NftUrl(pydantic.BaseModel):
    original: str
    h250: Optional[str]
    h500: Optional[str]
    h750: Optional[str]
    h1000: Optional[str]


class NftMetadata(pydantic.BaseModel):
    owner: Optional[str]
    chain: str  # ethereum, klaytn, polygon, binance
    contract_address: str
    token_id: str
    token_type: str
    source_url: Optional[NftUrl]  # caching 데이터 url
    content_type: Optional[str]  # caching 데이터의 mime type
    name: str
    description: Optional[str]
    image: Optional[str]  # token uri 상의 NFT image. (http, IPFS, raw data)
    animation_url: Optional[str]  # opensea 의 video, music nft 의 source url
    external_url: Optional[str]
    attributes: Optional[List[NftAttribute]]
    token_data: Optional[dict]  # nft 원본 데이터
    cached: bool = True  # cache 데이터인지 ? API 데이터인지

    def __str__(self) -> str:
        return f"[{self.chain} - {self.token_type}] {self.name} - {self.contract_address} - {self.token_id}"


class NftResponse(pydantic.BaseModel):
    cursor: Optional[str]
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
