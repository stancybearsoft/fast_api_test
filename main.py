import uvicorn
from fastapi import FastAPI

from core.models.database import Base, engine
from api_v1.routers import vin_codes


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sample FastAPI Application",
              description="Sample FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0", )

app.include_router(vin_codes.router, prefix="/v1")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
