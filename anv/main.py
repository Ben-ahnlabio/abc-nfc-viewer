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
    cursor: str = None,
    resync: bool = False,
):
    nft_service = app_config.get_nft_service()
    owned_nfts_result = nft_service.get_NFTs_by_owner(
        chain=chain, owner=owner, cursor=cursor, resync=resync
    )

    task_list = list(filter(lambda nft: nft.source_url is None, owned_nfts_result.nfts))
    background_tasks.add_task(cache_nft_source_list, task_list)

    return models.NftResponse(
        items=owned_nfts_result.nfts, cursor=owned_nfts_result.cursor
    )


def cache_nft_source_list(nft_list: List[models.NftMetadata]):
    """nft metadata 의 url 항목이 None 이면 cache 작업을 시작한다."""
    with futures.ThreadPoolExecutor(max_workers=5) as exec:
        future_to_nft = {exec.submit(cache_nft_source, nft): nft for nft in nft_list}
        for f, nft in future_to_nft.items():
            try:
                _ = f.result()
            except Exception as e:
                log.error("cache nft source error. %s. nft=%s", e, nft)


def cache_nft_source(nft: models.NftMetadata):
    repo = app_config.get_nft_src_repository()
    repo.cache_nft_source(nft)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
