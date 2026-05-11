from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean
from sqlalchemy.sql import func

from app.core.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    filename = Column(String, nullable=False)

    file_type = Column(String, nullable=True)

    status = Column(String, default="uploaded")

    extracted_data = Column(JSON, nullable=True)

    reviewed_data = Column(JSON, nullable=True)

    is_finalized = Column(Boolean, default=False)

    retry_count = Column(Integer, default=0)

    error_message = Column(String, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )