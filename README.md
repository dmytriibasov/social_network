# Social Network simple project

## General Info
The project is based on Django Rest Framework and contains the basic functionality of 
creating users, authentication and posts creating API`s.

## Technologies
1. Django (DRF)
2. Simple JWT
3. Redis
4. Celery
5. Postgres

## Installation
### Before running the project
- Firstly install [docker-compose](https://docs.docker.com/compose/install/)
- Create an empty `.env` file in your project folder
- Configure your `.env` file (you can find `.env.example` file)
- build containers: `docker-compose build`
- run project: `docker-compose up`

**ports: 5432, 8000, 8080 must be available!** (or configure them in `docker-compose` file)

If you want to stop the project, just run: `docker-compose down`
