from envparse import Env


env = Env()

PROD_DB_URL = env.str(
    "PROD_DB_URL",
    default="postgresql+asyncpg://axkxd:ksflsncGdsK@localhost:5432/postgres"
)
