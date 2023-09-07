from envparse import env

env.read_envfile()

API_HOST = env.str("API_HOST", default="http://localhost:8080/")

DB_URL = env.str("DB_URL", default="postgresql://lule@localhost/lule")

# Storage
BUCKET_NAME = env.str("BUCKET_NAME", default="lule")
S3_ENDPOINT_URL = env.str("S3_ENDPOINT_URL")
S3_ACCESS_KEY_ID = env.str("S3_ACCESS_KEY_ID")
S3_SECRET_ACCESS_KEY = env.str("S3_SECRET_ACCESS_KEY")
