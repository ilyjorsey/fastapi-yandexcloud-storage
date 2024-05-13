rm:
	docker-compose stop \
	&& docker-compose rm 

up:
	docker-compose -f docker-compose.yml up --force-recreate

