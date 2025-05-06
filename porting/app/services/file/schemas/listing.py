from pydantic import BaseModel

class S3FileEntry(BaseModel):
    key: str
    size: int
    last_modified: str

    class Config:
        schema_extra = {
            "example": {
                "key": "uploads/2025/file1.png",
                "size": 123456,
                "last_modified": "2025-05-06T10:00:00"
            }
        }
