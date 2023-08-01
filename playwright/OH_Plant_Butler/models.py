import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, inspect

db_path = os.path.dirname(os.path.realpath(__file__))
connection_string = "sqlite:///" + os.path.join(db_path, 'plant.db')
engine = create_engine(
    connection_string, connect_args={"check_same_thread": False}, pool_size=50)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def oh_butler_database_tables():

    # database models
    class ButlerRecorder(Base):
        __tablename__ = "oh_butler_recorder_table"
        __table_args__ = {'extend_existing': True}

        id = Column(Integer, primary_key=True, index=True)
        jobid = Column(String, nullable=False)
        receipt = Column(String, nullable=True)
        instrument_status = Column(String, nullable=True)
        document_type = Column(String, nullable=True)
        document_number = Column(String, nullable=True)
        book_type = Column(String, nullable=True)
        recording_date = Column(String, nullable=True)
        grantor = Column(String, nullable=True)
        grantee = Column(String, nullable=True)
        legal_des = Column(String, nullable=True)
        long_desc = Column(String, nullable=True)
        document_pages = Column(String, nullable=True)
        signature_pages = Column(String, nullable=True)
        book = Column(String, nullable=True)
        page = Column(String, nullable=True)
        consideration = Column(String, nullable=True)
        related_doc = Column(String, nullable=True)
        data_extract_status = Column(Integer, default=0)
        pdf_status = Column(Integer, default=0)

    if not inspect(engine).has_table('oh_butler_recorder_table'):
        Base.metadata.create_all(bind=engine, checkfirst=True)

    class ButlerStatus(Base):
        __tablename__ = "oh_butler_status_table"
        __table_args__ = {'extend_existing': True}

        jobid = Column(String, primary_key=True, index=True)
        state = Column(String, nullable=False)
        county = Column(String, nullable=False)
        status = Column(Integer, nullable=False)  # 1 running, 2 completed, 3 error
        from_date = Column(String, nullable=False)
        thru_date = Column(String, nullable=False)
        total_record_found = Column(Integer, nullable=True)
        total_record_extracted = Column(Integer, nullable=True)
        missing_records = Column(Integer, nullable=True)
        total_pdf_downloaded = Column(Integer, nullable=True)
        pdf_not_found = Column(Integer, nullable=True)

    if not inspect(engine).has_table('oh_butler_status_table'):
        Base.metadata.create_all(bind=engine, checkfirst=True)

    return ButlerRecorder, ButlerStatus, sessionLocal

