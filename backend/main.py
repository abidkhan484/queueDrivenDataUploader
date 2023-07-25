from fastapi import FastAPI, UploadFile, File, Request, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from os import getenv
from dotenv import load_dotenv
from models import UploadData


load_dotenv()

app = FastAPI()
log_dir = getenv("LOG_PATH")
logging.basicConfig(filename=f"{log_dir}/access.log", level=logging.INFO)

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


@app.post("/upload/{file_unique_name}", status_code=status.HTTP_201_CREATED)
def upload_file(file_unique_name: str = "", data: UploadFile = File(...), response: Response = None):
    try:
        chunk_raw_content = data.file.read()
        if (chunk_raw_content):
            chunk_content = chunk_raw_content.decode("utf-8")
            logging.info(file_unique_name)
            logging.info(chunk_content)
            from tasks import write_chunk_file
            write_chunk_file.delay(file_unique_name, chunk_content)
    except Exception as e:
        logging.debug(str(e))
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"message": "There was an error uploading the file"}

    return {"isSuccess": True, "message": f"Successfully uploaded {file_unique_name} file"}

@app.post("/upload/complete", status_code=status.HTTP_201_CREATED)
def upload_complete(data: UploadData, response: Response = None):
    try:
        file_unique_name = data.file_unique_name
        # write the code to merge the files and delete the chunk files
        return {"isSuccess": True, "message": f"Successfully uploaded {file_unique_name} file"}
    except Exception as e:
        print(str(e))
        logging.debug(str(e))
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return {"message": "There was an error uploading the file"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=getenv("SERVER_PORT"),
                log_level="info", reload=True)
