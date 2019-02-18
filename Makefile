up:
	docker-compose build
	docker-compose up

clean:
	docker-compose rm -vsf
	docker volume rm lava-server-pgdata
	docker volume rm squad-home
	docker volume rm worker-http
	docker volume rm worker-tftp

