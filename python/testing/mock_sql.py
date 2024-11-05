import time
from datetime import datetime

from sqlalchemy import create_engine, Column, Integer, String, Boolean,BIGINT,TIMESTAMP
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from CustomException import CustomException

# Daca devine enervant warningu ala
# import warnings
# warnings.filterwarnings("ignore")
file_path = 'mocks.db'
engine = create_engine(f'sqlite:///{file_path}',echo=True)
Base = declarative_base()


class Mock(Base):
    __tablename__ = 'mocks'
    id = Column(Integer, primary_key=True)
    km = Column(Integer)

class MockAdd(Base):
    __tablename__ = 'mockadds'
    id = Column(Integer, primary_key=True)
    userid = Column(Integer)
    modifenum= Column(Integer)
    timestamp = Column(TIMESTAMP)
    details = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def initializeModifykmMock():
    session.add(Mock(id=1, km=1))
    session.commit()

def startModifykmMock():
    start_time = time.time()
    end_time = start_time + 60
    km = 2
    i = 0
    while time.time() < end_time:
        modifykm(km)
        km += 1
        i += 1
    print(km)
    print("changes", i)
    session.commit()
    session.close()
def modifykm(km):
    mock = session.query(Mock).filter_by(id=1).first()
    last_km = mock.km
    mock.km = km
    session.add(MockAdd(userid=1,modifenum=1,timestamp=datetime.fromtimestamp(1715374830.634419),details=f"km modified from {last_km} to {km}"))
    session.commit()

startModifykmMock()