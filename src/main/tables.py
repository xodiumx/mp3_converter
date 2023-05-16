from sqlalchemy import (
    Column, Date, Integer, MetaData,
    String, Table,)

metadata = MetaData()


quiz = Table(
    'quiz',
    metadata,
    Column('pk', Integer, primary_key=True),
    Column('id', Integer, unique=True, nullable=False),
    Column('question', String(512), nullable=False, index=True,),
    Column('answer', String(512), nullable=False, index=True,),
    Column('created_at', Date, nullable=False, index=True,),
)
