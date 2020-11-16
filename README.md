### Running

1)
```
docker-compose up -d --build
```

2)
```
docker-compose run web python manage.py makemigrations
docker-compose run web python manage.py migrate
```
OR
```
docker exec -it web bash 
python manage.py makemigrations
python manage.py migrate
```

### Creating first user
```
docker-compose run web python manage.py createsuperuser
```
OR
```
docker exec -it web bash
python manage.py createsuperuser
```

### Testing
```
docker-compose run web python manage.py test
```
OR
```
docker exec -it web bash
python manage.py manage.py test
```

#### Containers
   * `web`: API running on port [`8081`](http://localhost:8081/api/)
   * `db`: MySQL database running on port `3009`


### Documentation
   [`doc`](http://localhost:8081/docs/)
