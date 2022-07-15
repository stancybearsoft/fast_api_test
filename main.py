import os

import uvicorn
from fastapi import FastAPI, Path

from models.async_db_session import AsyncDatabaseSession
from models.init_default_data import init_default_data
from models.pydantic_models import VinCodeResponse
from models.tabs import VinCodes

app = FastAPI()

database_uri = os.getenv(
    'DATABASE_URL', 'postgres://postgres:example@localhost:5432/fast_api_test')
database_uri = database_uri.replace('postgres://', 'postgresql+asyncpg://')

db_session = AsyncDatabaseSession(database_uri)


@app.on_event("startup")
async def startup():
    await db_session.init()
    await init_default_data(db_session)


@app.on_event("shutdown")
async def shutdown():
    await db_session.close()


@app.get("/v1/vehicle/get/{vin_code}", response_model=VinCodeResponse)
async def get_vin_code_info(vin_code: str = Path(default="4Y1SL65848Z411439",
                                                 description="4Y1SL65848Z411439",
                                                 min_length=17, max_length=17)):
    """
    returns information about vehicle by vin code
    """
    result = await VinCodes.get_vin_code_info(session=db_session, vin_code=vin_code)
    return result


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
