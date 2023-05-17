from sqlalchemy import (UUID, Boolean, Column, Date, ForeignKey, Integer,
                        LargeBinary, MetaData, String, Table)

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

user = Table(
    'user',
    metadata,
    Column('id', UUID, primary_key=True),
    Column(
        'email', String(128), unique=True, nullable=False, index=True,),
    Column(
        'hashed_password', String(128), nullable=False,
    ),
    Column(
        'is_active', Boolean(), default=True, nullable=False,
    ),
    Column(
        'is_superuser', Boolean, default=False, nullable=False,
    ),
    Column(
        'is_verified', Boolean, default=False, nullable=False,
    )
)

audio_file = Table(
    'audio_file',
    metadata,
    Column('id', UUID, primary_key=True),
    Column('user', UUID, ForeignKey('user.id', ondelete='CASCADE')),
    Column('filename', String(64), nullable=False, unique=True),
    Column('file_path', String(64), nullable=False, unique=True),
    Column('data', LargeBinary(), nullable=False,),
)
