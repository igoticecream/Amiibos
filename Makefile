IMAGE_NAME="amiibo"
CONTAINER_NAME="amiibo-container"

all: build
	@docker run -it --rm --volume "${CURDIR}/data:/app/data" --name ${CONTAINER_NAME} ${IMAGE_NAME}

build:
	@docker build --rm --tag ${IMAGE_NAME} .

count:
	@find data -type f -name amiibo.json | wc -l
