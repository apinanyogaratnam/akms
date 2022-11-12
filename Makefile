VERSION := 0.1.0
IMAGE := akms

start:
	uvicorn api.main:app --reload

create_db:
	python create_api_keys_db.py

format:
	black .
	isort .

workflow:
	git tag -m "v${VERSION}" v${VERSION}
	git push --tags

build:
	docker build -t ${IMAGE} .
