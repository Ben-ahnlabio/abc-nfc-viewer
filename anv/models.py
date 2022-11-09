import enum
from typing import List, Optional

import pydantic


class Network(enum.Enum):
    ETHEREUM = "Ethereum"
    KLAYTN = "Klaytn"
    POLYGON = "Polygon"
    BINANCE = "Binance"


class NftAttribute(pydantic.BaseModel):
    trait_type: str
    value: str


class NftMetadata(pydantic.BaseModel):
    network: str
    contract_address: str
    token_id: str
    token_type: str
    name: str
    description: Optional[str]
    image: Optional[str]
    url: Optional[pydantic.HttpUrl]
    attributes: Optional[List[NftAttribute]]
    cached: bool = True  # cache 데이터인지 ? API 데이터인지

    def __str__(self) -> str:
        return f"[{self.network} - {self.token_type}] {self.name} - {self.description}"


class NftResponse(pydantic.BaseModel):
    owner: str  # wallet address
    network: Network  # ethereum, klaytn, polygon, binance
    nfts: Optional[List[NftMetadata]]


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
