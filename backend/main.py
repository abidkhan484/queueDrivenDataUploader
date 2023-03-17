from fastapi import FastAPI, UploadFile, File, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from os import getenv
from dotenv import load_dotenv


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
        print(str(e))
        logging.debug(str(e))
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"message": "There was an error uploading the file"}

    return {"isSuccess": True, "message": f"Successfully uploaded {file_unique_name} file"}

@app.post("/upload/complete", status_code=status.HTTP_200_OK)
def upload_complete(request: Request, response: Response = None):
    return {"isSuccess": True, "message": f"Successfully uploaded {file_unique_name} file"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000,
                log_level="info", reload=True)
