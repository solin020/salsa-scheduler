from dataclasses import dataclass
from datetime import datetime, timedelta
from fastapi import Request
from sqlalchemy.types import JSON, TEXT, ARRAY
from sqlalchemy.schema import Column
from sqlmodel import Field, SQLModel, text
import sqlalchemy
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from config import db_username, db_password, db_host, db_name






@dataclass
class Admin(SQLModel, table=True):
    __tablename__ = "admins"
    id: str = Field(primary_key=True)

@dataclass
class Coordinator(SQLModel, table=True):
    __tablename__ = "coordinators"
    projects: list[str] = Field(sa_column=Column(ARRAY(TEXT)))
    id: str = Field(primary_key=True)

@dataclass
class Annotator(SQLModel, table=True):
    __tablename__ = "annotators"
    projects: list[str] = Field(sa_column=Column(ARRAY(TEXT)))
    id: str = Field(primary_key=True)

@dataclass
class Participant(SQLModel, table=True):
    __tablename__ = "participants"
    projects: list[str] = Field(sa_column=Column(ARRAY(TEXT)))
    id: str = Field(primary_key=True)
    phone_number: str


@dataclass
class TestPrototype(SQLModel, table=True):
    project: str
    id: str = Field( primary_key=True)



@dataclass
class MessageSchedule(SQLModel, table=True):
    __tablename__ = 'message_schedule'
    project: str
    tries: int
    max_tries: int
    message: str
    participant_id:str
    source_number: str
    dest_number: str
    account_sid: str
    auth_token: str
    test_prototype_id: str
    schedule_id: str = Field(primary_key=True)
    time: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    bug_interval: timedelta = Field(sa_column=Column(sqlalchemy.types.Interval))

@dataclass
class MessageResponse(SQLModel, table=True):
    project: str
    schedule_id: str = Field(primary_key=True)
    participant_id: str
    timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    miscellaneous: dict = Field(sa_column=Column(JSON), default={})
    test_prototype_id: str

@dataclass
class ResponseAnnotation(SQLModel, table=True):
    project: str
    schedule_id: str = Field(primary_key=True)
    annotator_id: str
    annotation_file: str
    timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))







url = f'''postgresql+asyncpg://{db_username}:{db_password}@{db_host}/{db_name}'''

async_engine =  create_async_engine(url,
                                    echo=True,
                                    pool_size=10,
                                    pool_pre_ping=True,
                                    max_overflow=0,
                                    future=True)
async def get_db(r:Request) -> AsyncSession: # type: ignore
    email = r.headers.get('salsaid')
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False,
        autocommit=False, autoflush=False
    )
    async with async_session() as session:
        await session.execute(text(f'CALL salsa_login(:x)'), {'x':email})
        yield session


async def update_users(): # type: ignore
    async_session = async_sessionmaker(
        bind=async_engine, class_=AsyncSession, expire_on_commit=False,
        autocommit=False, autoflush=False
    )
    async with async_session() as session:
        await session.exec(text('CALL update_users()'))