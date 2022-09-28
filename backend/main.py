from fastapi import FastAPI, Body, UploadFile, File, Request
from fastapi.middleware.cors import CORSMiddleware
import logging

app = FastAPI()
logging.basicConfig(filename='access.log', level=logging.DEBUG)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/upload/{fileUniqueName}", status_code=201)
def upload_file(fileUniqueName: str, request: Request):
    try:
        data: bytes = request.body()
        logging.debug(data)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        print("done")
    return {"message": f"Successfully uploaded {fileUniqueName}"}


