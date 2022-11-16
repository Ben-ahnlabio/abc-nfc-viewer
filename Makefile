deploy:
	gcloud app deploy app.yml --project abc-nft-368700

run:
	uvicorn anv.main:app --reload