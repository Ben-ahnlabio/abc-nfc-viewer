# NFT Viewer

지갑주소와 network(ethereum, klaytn, polygon, binance) 를 입력받아 지갑 사용자가 보유한 NFT Metadata 를 출력

## NFT Metadata

하나의 NFT 에 대한 데이터. metadata 는 아래 표 형식으로 구성됨.

| Key              | Description                                        |
| ---------------- | -------------------------------------------------- |
| network          | `ethereum`, `klaytn`, `polygon`, `binance` 중 하나 |
| contract_address | NFT 의 contract 주소                               |
| token_id         | NFT 의 token id                                    |
| token_type       | NFT 의 token type                                  |
| name             | 이름                                               |
| description      | 설명                                               |
| image            | NFT 데이터 (아래 `image` 설명 참고)                |
| animation_url    | video, music NFT 의 source URL                     |
| url              | 크기별 데이터 url (아래 `animation_url` 설명 참고) |
| attributes       | NFT attributes                                     |

각 키값에 대한 설명은 아래

### network

ABC extension 지갑에서 지원하는 blockchain network. `ethereum`, `klaytn`, `polygon`, `binance` 중 하나가 될 수 있음.

### contract_address

NFT 의 contract_address. `0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb` 와 같은 형태.

### token type

해당 NFT 의 token type. [ERC1155](https://ethereum.org/ko/developers/docs/standards/tokens/erc-1155/), [ERC721](https://ethereum.org/ko/developers/docs/standards/tokens/erc-721/), [KIP-17](https://kips.klaytn.foundation/KIPs/kip-17) 등의 값을 가질 수 있음.

### image

NFT 의 데이터 이미지. http URL, IPFS URL, 이미지 데이터 자체가 들어있을 수 있음. 아래 예시 참고.

https URL 인 경우 연결이 느리거나 이미지가 없을 수 있음.

IPFS URL 인 경우 직접 접근 불가. download 후 caching 필요.

#### IPFS

`ipfs://QmdKr7nXPdizGqV65t9viyu7QtwJdPBExXL8CapUqULbBL`

#### http

`https://miya.sunmiya.club/6727.png`

#### raw data

```
data:image/svg+xml;utf8,<svg xmlns=\"http://www.w3.org/2000/svg\" version=\"1.2\" viewBox=\"0 0 24 24\"><rect x=\"8\" y=\"4\" width=\"1\" height=\"1\" shape-rendering=\"crispEdges\" fill=\"#000000ff\"/>...</svg>
```

### animation_url

video, music NFT 인 경우. MP4, MP3 URL 값.

### url

NFT image resize URL. 이미지 resize 작업 후 이 데이터가 추가됨.

video, music NFT 인 경우 (`animation_url` 이 있는 경우) 이 데이터가 없을 수 있음.

```json
{
  "url": {
    "original": "https://miya.sunmiya.club/6727.png",
    "small": "https://dizGqV6.com/QmdKr7nXPdizGq/small.png",
    "large": "https://dizGqV6.com/QmdKr7nXPdizGq/large.png"
  }
}
```

### attributes

NFT 속성을 나타내는 값. 아래는 `CryptoPunks` NFT 중 하나의 attributes 값 예시.

```json
{
  "attributes": [
    {
      "trait_type": "type",
      "value": "Male 3"
    },
    {
      "trait_type": "attribute",
      "value": " Mustache"
    }
  ]
}
```

## API Reference

### 특정 지갑 사용자가 보유한 NFT 목록 조회

```http
  GET /v1/nfts/{chain}
```

#### Path Parameter

| Parameter | Type     | Description                                                           |
| :-------- | :------- | :-------------------------------------------------------------------- |
| `chain`   | `string` | **Required** chain `ethereum`, `klaytn`, `polygon`, `binance` 중 하나 |

#### Query Parameter

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `owner`   | `string` | **Required** owner wallet address |

#### 호출 예시

```bash
curl --url 'http://localhost:8000/v1/nfts/ethereum?owner=0x0232d1083E970F0c78f56202b9A666B526FA379F
```

## env

| Key                          | Description                                                  |
| ---------------------------- | ------------------------------------------------------------ |
| KAS_CREDENTIAL_JSON_PATH     | kas credential json 파일 경로                                |
| KAS_ACCESS_KEY_ID            | kas credential 값. KAS_CREDENTIAL_JSON_PATH 있는 경우 불필요 |
| KAS_AUTHORIZATION            | kas credential 값. KAS_CREDENTIAL_JSON_PATH 있는 경우 불필요 |
| KAS_SECRET_ACCESS_KEY        | kas credential 값. KAS_CREDENTIAL_JSON_PATH 있는 경우 불필요 |
| ALCHEMY_ETHER_MAIN_API_KEY   | alchemy ether main net api key                               |
| ALCHEMY_POLYGON_MAIN_API_KEY | alchemy polygon main net api key                             |
| MORALIS_API_KEY              | moralis api key                                              |

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

현재 구현 : 일단 첫 조회시 metadata 업데이트를 요청함. 요청 직후에는 데이터가 없어 오류 발생으로 제외됨. 나중에 다시 해당 NFT 를 조회하면 정상

### music, video nft

image NFT 가 아닌 music 이나 video NFT 인 경우는 NFT metadata 에 `image` 항목이 존재하지 않을 수 있음

대신 `animation_url` 이 존재함. 또는 둘다 있을 수도 있음.

animation_url 인 경우 `<video>` 로 출력해야 함.

아래는 metadata 에 image 가 존재하지 않는 경우임

https://opensea.io/assets/ethereum/0x008c69e0c66ebd4b228d27f2162ad54ab1b7dde1/413

```json
{
  "contract": { "address": "0x008C69E0c66EbD4b228D27F2162aD54AB1b7dDE1" },
  "id": { "tokenId": "413", "tokenMetadata": { "tokenType": "ERC721" } },
  "title": "Bivouac - GOLD",
  "description": "BIG3 Ownership is an innovative, new approach to team ownership in professional sports. The league is creating a new model of ownership by leveraging blockchain technology to sell NFTs that represent ownership-like value in its twelve teams. All editions include voting rights towards team actions, priceless gameday experiences and VIP tickets to all games, and limited-edition team, league, and championship merchandise and memorabilia. Fire editions also include exclusive intellectual property and licensing rights to team names, logos, and merchandise as well as additional gameday activations.",
  "tokenUri": {
    "raw": "https://ownership.big3.com/apis/pages/getnft/413/13/2",
    "gateway": "https://ownership.big3.com/apis/pages/getnft/413/13/2"
  },
  "media": [{ "raw": "", "gateway": "" }],
  "metadata": {
    "name": "Bivouac - GOLD",
    "description": "BIG3 Ownership is an innovative, new approach to team ownership in professional sports. The league is creating a new model of ownership by leveraging blockchain technology to sell NFTs that represent ownership-like value in its twelve teams. All editions include voting rights towards team actions, priceless gameday experiences and VIP tickets to all games, and limited-edition team, league, and championship merchandise and memorabilia. Fire editions also include exclusive intellectual property and licensing rights to team names, logos, and merchandise as well as additional gameday activations.",
    "animation_url": "https://ownership.big3.com/apis/metadata/render/GOLD/Bivouac_GOLD.mp4",
    "attributes": []
  },
  "timeLastUpdated": "2022-11-10T01:18:18.921Z",
  "contractMetadata": {
    "name": "BIG3 Ownership",
    "symbol": "BIG3",
    "totalSupply": "582",
    "tokenType": "ERC721",
    "openSea": {
      "floorPrice": 0.99,
      "collectionName": "Official BIG3 Ownership",
      "safelistRequestStatus": "verified",
      "imageUrl": "https://i.seadn.io/gae/HTyypf6ylK_ns_U5_cY-AqJz5Fr4rJlSNDQsROKJnShKr7pR7MDRC1utJziKaxuscGCx0kKmK2PiqHorxeSMVB-STMpnzYKl-5W_?w=500&auto=format",
      "description": "BIG3 Ownership is an innovative, new approach to team ownership in professional sports. The league is creating a new model of ownership by leveraging blockchain technology to sell NFTs that represent ownership-like value in its twelve teams.\n\n\nAll editions include voting rights towards team actions, priceless gameday experiences and VIP tickets to all games, and limited-edition team, league, and championship merchandise and memorabilia. Fire editions also include exclusive intellectual property and licensing rights to team names, logos, and merchandise as well as additional gameday activations.\n",
      "externalUrl": "https://big3.com",
      "twitterUsername": "BIG3Ownership",
      "discordUrl": "https://discord.gg/big3",
      "lastIngestedAt": "2022-11-07T21:29:51.000Z"
    }
  }
}
```

아래는 `image` 와 `animation_url` 이 둘다 존재하는 경우임

```json
{
  "contract": { "address": "0x495f947276749Ce646f68AC8c248420045cb7b5e" },
  "id": {
    "tokenId": "16964895045191086691836525954255352035824775810036846025640728189214883053569",
    "tokenMetadata": { "tokenType": "ERC1155" }
  },
  "title": "Crypto ballad NFT mp3",
  "description": "Beautiful lyrical music. A romantic melody for love. Audio NFT music mp3 for sale",
  "tokenUri": {
    "raw": "https://api.opensea.io/api/v1/metadata/0x495f947276749Ce646f68AC8c248420045cb7b5e/0x{id}",
    "gateway": "https://api.opensea.io/api/v1/metadata/0x495f947276749ce646f68ac8c248420045cb7b5e/16964895045191086691836525954255352035824775810036846025640728189214883053569"
  },
  "media": [
    {
      "raw": "https://i.seadn.io/gae/nTzi6DQxP_5A1SkQ76PPwl1z0RHLijfMOJxvpU-UGThZHZK4zFqwZoNrSNmSvAGWfEif_rmP4SybBQ0e2ZI-p4ph8v01oGLBo8krcuw?w=500&auto=format",
      "gateway": "https://i.seadn.io/gae/nTzi6DQxP_5A1SkQ76PPwl1z0RHLijfMOJxvpU-UGThZHZK4zFqwZoNrSNmSvAGWfEif_rmP4SybBQ0e2ZI-p4ph8v01oGLBo8krcuw?w=500&auto=format"
    }
  ],
  "metadata": {
    "name": "Crypto ballad NFT mp3",
    "description": "Beautiful lyrical music. A romantic melody for love. Audio NFT music mp3 for sale",
    "image": "https://i.seadn.io/gae/nTzi6DQxP_5A1SkQ76PPwl1z0RHLijfMOJxvpU-UGThZHZK4zFqwZoNrSNmSvAGWfEif_rmP4SybBQ0e2ZI-p4ph8v01oGLBo8krcuw?w=500&auto=format",
    "animation_url": "https://openseauserdata.com/files/b4c01700e1ead2d8c6b02f780689c8d7.mp3"
  },
  "timeLastUpdated": "2022-11-10T01:31:59.441Z",
  "contractMetadata": {
    "name": "OpenSea Shared Storefront",
    "symbol": "OPENSTORE",
    "tokenType": "ERC1155",
    "openSea": {
      "floorPrice": 0.0,
      "collectionName": "OS Shared Storefront Collection",
      "safelistRequestStatus": "not_requested",
      "imageUrl": "https://openseauserdata.com/files/860b94bee079e3864d04849383d2b4d1.bin",
      "description": "",
      "lastIngestedAt": "2022-11-08T16:09:10.000Z"
    }
  }
}
```

### image 값이 ipfs gateway(http) 인데 연결이 되지 않는 경우

다른 ipfs gateway service 를 사용하여 이미지 출력

### image 값이 'data:image/svg+xml;utf8' 로 시작하는 raw data 인경우

svg 부분을 따로 떼어 png 로 저장하고 caching
