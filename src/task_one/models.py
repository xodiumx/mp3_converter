from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class QuizModel(Base):
    
    __tablename__ = 'quiz'

    pk: Mapped[int] = mapped_column(
        Integer, primary_key=True,
    )
    id: Mapped[int] = mapped_column(
        Integer, unique=True, nullable=False
    )
    question: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True,
    )
    answer: Mapped[str] = mapped_column(
        String(512), nullable=False, index=True,
    )
    created_at: Mapped[Date] = mapped_column(
        Date, nullable=False, index=True,
    )
