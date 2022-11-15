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
async def get_nft_by_owner_v2(chain: models.Chain, owner: str, resync: bool = False):
    nft_service = app_config.get_nft_service()
    nft_metadata = nft_service.get_NFTs_by_owner(
        chain=chain, owner=owner, resync=resync
    )
    return models.NftResponse(items=nft_metadata)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
