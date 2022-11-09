from fastapi import FastAPI

from anv import models

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "nft viewer api"}


@app.get("/nfts/{owner}/{network}", response_model=models.NftResponse)
async def nfts(owner: str, network: models.Network = None):
    return models.NftResponse(owner=owner, network=network)


def main() -> None:
    pass


if __name__ == "__main__":
    main()
