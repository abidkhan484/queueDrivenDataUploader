from pydantic import BaseModel

class UploadData(BaseModel):
    file_unique_name: str
