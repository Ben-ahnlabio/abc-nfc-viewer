# deploy google cloud platform app engine
deploy_gae:
	cp anv/.env.production anv/.env
	poetry export --without-hashes --format=requirements.txt > requirements.txt
	gcloud app deploy app.yml --project abc-nft-368700
	cp anv/.env.dev anv/.env

# run debug server
run:
	uvicorn anv.main:app --reload --workers 8