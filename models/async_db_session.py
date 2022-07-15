from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker


Base = declarative_base()


class AsyncDatabaseSession:
    def __init__(self, connection_string: str):
        self._session = None
        self._engine = None
        self._connection_string = connection_string

    def __getattr__(self, name):
        return getattr(self._session, name)

    async def init(self):
        self._engine = create_async_engine(self._connection_string, echo=True)
        session = sessionmaker(
            self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
        self._session = session()

    async def create_all(self, base=Base) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)
