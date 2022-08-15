import os


SQLALCHEMY_DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://postgres:example@localhost:5432/fast_api')

TEST_DATABASE_URL = os.getenv(
    'DATABASE_URL', 'postgresql://postgres:example@localhost:5432/fast_api_test')

