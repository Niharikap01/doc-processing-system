from pydantic import BaseModel
from typing import Optional

class DocumentResponse(BaseModel):
    id: int
    filename: str
    status: str
    extracted_data: Optional[str]

    class Config:
        from_attributes = True