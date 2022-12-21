VERSION := 1.1.0
IMAGE := akms
REGISTRY_URL := ghcr.io/apinanyogaratnam/${IMAGE}
IMAGE_VERSION_NAME := ${REGISTRY_URL}:${VERSION}
IMAGE_LATEST_VERSION_NAME := ${REGISTRY_URL}:latest

install:
	pip install pipenv==2022.11.5
	pipenv install

start:
	python main.py

up:
	docker-compose up --build

test:
	pytest .

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

tag-image:
	docker tag ${IMAGE} ${IMAGE_LATEST_VERSION_NAME}
	docker tag ${IMAGE} ${IMAGE_VERSION_NAME}

push-image:
	docker push ${IMAGE_LATEST_VERSION_NAME}
	docker push ${IMAGE_VERSION_NAME}
