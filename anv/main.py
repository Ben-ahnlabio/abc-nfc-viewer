import logging

import dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from anv import api, config, models

log = logging.getLogger("anv")
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

dotenv.load_dotenv()

app = FastAPI()
app_config = config.AppConfig()

origins = [
    "*"
    # "http://localhost",
    # "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    log.debug("GET /")
    return {"message": "nft viewer api"}


@app.get("/v1/nfts/{chain}", response_model=models.NftResponse)
async def get_nft_by_owner(
    chain: models.Chain,
    owner: str,
    page: int = 1,
    per_page: int = 20,
    resync: bool = False,
):
    chain_map = {
        models.Chain.ETHEREUM: app_config.get_ethereum_api(),
        models.Chain.POLYGON: app_config.get_polyfon_api(),
        models.Chain.KLAYTN: app_config.get_klaytn_api(),
    }

    nft_api: api.ChainNetData = chain_map[chain]
    nft_metadata = nft_api.get_NFTs_by_owner(owner, resync)

    repo = app_config.get_nft_src_repository()
    for data in nft_metadata:
        data.url = repo.get_nft_cached_urls(data.image)

    return models.NftResponse(page=page, per_page=per_page, items=nft_metadata)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
