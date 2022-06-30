# How to run

## Local
1. Create `.env` file with the content matching `.env.example`. Set `DB_STRING` value to something matching this structure `<server name>://<user name>:<user password>@<host>:<port>/<database name>`
2. Run migrations `alembic upgrade head`.
3. Run server `python run.py` 

## Docker

Install and configure Docker and docker-compose. 

1.Build and run containers:
```shell script
docker-compose up
```  
2.Connect to the app instance:

```shell script
docker exec -it jsp_project_web_1 bash
```

3.Change directory
```shell script
cd /code/
```

4.Run migrations
```shell script
alembic upgrade head
```