from concurrent import futures
import logging
from typing import List

import dotenv
from fastapi import FastAPI, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware

from anv import config, models

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
async def get_nft_by_owner_v1(
    chain: models.Chain,
    owner: str,
    background_tasks: BackgroundTasks,
    resync: bool = False,
):
    nft_service = app_config.get_nft_service()
    nft_metadata = nft_service.get_NFTs_by_owner(
        chain=chain, owner=owner, resync=resync
    )

    task_list = list(filter(lambda nft: nft.url is None, nft_metadata))
    for nft in task_list:
        background_tasks.add_task(cache_nft_source, nft)
    # background_tasks.add_task(cache_nft_source_list, task_list)

    return models.NftResponse(items=nft_metadata)


def cache_nft_source_list(nft_list: List[models.NftMetadata]):
    repo = app_config.get_nft_src_repository()
    with futures.ThreadPoolExecutor(max_workers=5) as exec:
        _ = {exec.submit(repo.cache_nft_source, nft) for nft in nft_list}


def cache_nft_source(nft: models.NftMetadata):
    repo = app_config.get_nft_src_repository()
    repo.cache_nft_source(nft)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
