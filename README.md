# NFT Viewer

지갑주소와 network(ethereum, klaytn, polygon, binance) 를 입력받아 소유중인 NFT 데이터를 출력

## env

`KAS_CREDENTIAL_JSON_PATH` 또는 `KAS_ACCESS_KEY_ID`, `KAS_AUTHORIZATION`, `KAS_SECRET_ACCESS_KEY` 필요

ALCHEMY_ETHER_MAIN_API_KEY
ALCHEMY_POLYGON_MAIN_API_KEY
ALCHEMY_SOLANA_MAIN_API_KEY
MORALIS_API_KEY

## issue

### token uri 가 http 경로인데 연결불가 인 경우

현재 구현 : 제외

```
KlaytnOwnedNft(contract_address='0xe27f0057aeec952fcfff4601b79bc2c114dac79e', token_id='0x54e6', owner='0xFE463e0d253Ea6972F13EA93516Da762503d0d2A', previous_owner='0x0000000000000000000000000000000000000000', token_uri='https://okaybearskr.com/json/21734.json', transaction_hash='0xfa0eef74f11e4a020eecaa042fa068aacd581f9392f129f4d353ee04a6a87fd9', updated_at=1660673462, created_at=None)
```

```
KlaytnOwnedNft(contract_address='0xe27f0057aeec952fcfff4601b79bc2c114dac79e', token_id='0x54e6', owner='0xFE463e0d253Ea6972F13EA93516Da762503d0d2A', previous_owner='0x0000000000000000000000000000000000000000', token_uri='https://okaybearskr.com/json/21734.json', transaction_hash='0xfa0eef74f11e4a020eecaa042fa068aacd581f9392f129f4d353ee04a6a87fd9', updated_at=1660673462, created_at=None)
```

### klaytn nft api

특정 NFT 토큰 정보 조회
https://refs.klaytnapi.com/ko/tokenhistory/latest#operation/getNftById

를 했을 때 tokenUri 데이터가 나오지 않는 경우가 있음

tokenUri 값이 없는 경우 예시

```json
{
  "tokenId": "0x2",
  "owner": "0xe5389503156ee02775ee18552f0c9d9846b66a91",
  "previousOwner": "0x0000000000000000000000000000000000000000",
  "tokenUri": "",
  "transactionHash": "0xc7d07066e4e42a7d896c34420ed43568ba44ae15a8ef771b13ba1f6f2\\ d2820c4",
  "createdAt": 1597304701,
  "updatedAt": 1597304701
}
```

tokenUri 에는 NFT 의 metadata 가 담겨있음. 아래는 tokenUri 데이터 예시

```json
{
  "name": "Infinity Door #934",
  "description": "A long journey begins, following the voice from somewhere. Infinity Door, consisting of 3 types per MIYA, will be randomly airdropped and MIYAs will warp transport to other planets respectively. The warp can be done by synthesizing Infinity Door, MIYA, and 280 Favor. The Synthesis schedule will be revealed after AMA.",
  "image": "https://limited-miya.sunmiya.club/door/undercity.png",
  "attributes": []
}
```

특정 NFT 토큰의 메타데이터 정보 업데이트
https://refs.klaytnapi.com/ko/tokenhistory/latest#operation/updateNFTTokenMetadata

를 호출하면 이후에는 tokenUri 가 출력되지만, 곧바로 갱신되지 않음.

현재 구현 : 제외
