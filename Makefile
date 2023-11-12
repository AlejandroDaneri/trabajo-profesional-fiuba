docker-image:
	docker build -f Dockerfile -t "algo_trading:latest" .
.PHONY: docker-image

docker-compose-up: docker-image
	docker-compose -f docker-compose.yml up --build
.PHONY: docker-compose-up