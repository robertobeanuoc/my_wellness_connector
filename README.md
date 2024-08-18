# whellness_conector
My whellness connector



# Update alembic model 

1. Load enviroment variables `source local_env.sh`
2. Generate auto upgrade `alembic revision --autogenerate -m "Initial migration"`
3. Sync database `alembic upgrade head`