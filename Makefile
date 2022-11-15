deploy:
	gcloud app deploy app.yml --project abc-nft

run:
	uvicorn anv.main:app --reload