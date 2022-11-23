deploy:
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	gcloud app deploy app.yml --project abc-nft-368700

run:
	uvicorn anv.main:app --reload --workers 8