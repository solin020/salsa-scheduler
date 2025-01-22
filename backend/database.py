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

           
    



#NOTE many of the primary key columns in this ORM are fake because the real primary keys
#are usually pairs of project and some other id column which SQLAlchemy cannot understand

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
    dropout: bool
    schedule_prototype_id: str
    schedule: dict = Field(sa_column=Column(JSON))
    twilio_nickname: str
    dashboard_code: str
    timezone: str



@dataclass
class TestPrototype(SQLModel, table=True):
    __tablename__ = "test_prototype"
    project: str
    id: str = Field( primary_key=True)
    groups: list[str] = Field(sa_column=Column(ARRAY(TEXT)))
    randomized:bool

@dataclass
class TwilioInfo(SQLModel, table=True):
    __tablename__ = "twilio_info"
    project: str
    account_sid: str
    auth_token: str 
    phone_number: str
    nickname: str = Field(primary_key=True)






@dataclass
class MessageSchedule(SQLModel, table=True):
    __tablename__ = 'message_schedule'
    project: str
    tries: int
    max_tries: int
    message: str
    participant_id:str
    twilio_info: str
    dest_number: str
    test_prototype_id: str
    sequence_no: int = Field(primary_key=True)
    time: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    bug_interval: timedelta = Field(sa_column=Column(sqlalchemy.types.Interval))

@dataclass
class SchedulePrototype(SQLModel, table=True):
    __tablename__ = "schedule_prototype"
    project: str
    id: str = Field(primary_key=True)
    schedule: dict = Field(sa_column=Column(JSON))
    


@dataclass
class StimulusResult(SQLModel, table=True):
    __tablename__ = "stimulus_result"
    project: str
    schedule_id: str = Field(primary_key=True)
    participant_id: str = Field(primary_key=True)
    formal_timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    real_timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    miscellaneous: dict = Field(sa_column=Column(JSON), default={})
    test_prototype_id: str = Field(primary_key=True)
    stimulus_id: str = Field(primary_key=True)
    sequence_no: int = Field(primary_key=True)
    quality: str
    schedule_prototype_id: str

@dataclass
class VisitResult(SQLModel, table=True):
    __tablename__ = "visit_result"
    project: str
    schedule_id: str = Field(primary_key=True)
    participant_id: str = Field(primary_key=True)
    formal_timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    real_timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    miscellaneous: dict = Field(sa_column=Column(JSON), default={})
    test_prototype_id: str = Field(primary_key=True)
    stimulus_id: str = Field(primary_key=True)
    sequence_no: int = Field(primary_key=True)
    quality: str
    schedule_prototype_id: str

@dataclass
class DownloadResult(SQLModel, table=True):
    __tablename__ = "download_result"
    project: str
    schedule_id: str = Field(primary_key=True)
    participant_id: str = Field(primary_key=True)
    formal_timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    real_timestamp: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=True)))
    miscellaneous: dict = Field(sa_column=Column(JSON), default={})
    test_prototype_id: str = Field(primary_key=True)
    stimulus_id: str = Field(primary_key=True)
    sequence_no: int = Field(primary_key=True)
    quality: str
    schedule_prototype_id: str




@dataclass
class Transcription(SQLModel, table=True):
    project: str
    schedule_id: str = Field(primary_key=True)
    stimulus_id: str
    segments: dict = Field(sa_column=Column(JSON), default={})
    score: float

@dataclass
class AllGroups(SQLModel, table=True):
    __tablename__ = 'all_groups'
    project: str
    group: str = Field(primary_key=True)


@dataclass
class MessageView(SQLModel, table=True):
    __tablename__ = 'message_view'
    participant_id: str = Field(primary_key=True)
    their_time: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=False), primary_key=True))
    utc_time: datetime = Field(sa_column=Column(sqlalchemy.types.DateTime(timezone=False), primary_key=True))
    message: str  = Field(primary_key=True)
    condition: str = Field(primary_key=True)
    sent: bool = Field(primary_key=True)

  
    



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
