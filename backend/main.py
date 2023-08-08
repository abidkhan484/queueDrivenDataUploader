from fastapi import FastAPI, UploadFile, File, Request, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
from os import getenv, listdir
from os.path import join
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
async def upload_file(file_unique_name: str = "", data: UploadFile = File(...), response: Response = None):
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

async def merge_files(file_unique_name, count):
    is_success = True
    if not count:
        return is_success

    try:
        file_path = join(getenv("TEMPORARY_FILE_PATH"), file_unique_name)
        with open(file_path, 'w') as outfile:
            for idx in range(count):
                input_file = join(getenv("TEMPORARY_FILE_PATH"), f"{file_unique_name}-"+str(idx))
                with open(input_file, 'r') as infile:
                    outfile.write(infile.read())
    except Exception as e:
        print(str(e))
        logging.debug(str(e))
        is_success = False

    return is_success

@app.post("/upload/complete/", status_code=status.HTTP_201_CREATED)
async def upload_complete(data: UploadData, response: Response = None):
    success = {"isSuccess": True, "message": "Successfully uploaded the file"}
    error = {"message": "There was an error uploading the file"}
    try:
        file_unique_name = data.file_unique_name
        file_path = getenv("LOG_PATH")
        count = len([filename for filename in listdir(file_path) if filename.startswith(file_unique_name)])
        is_success = await merge_files(file_unique_name, count)
        if is_success:
            output = success
        else:
            output = error
            response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    except Exception as e:
        print(str(e))
        logging.debug(str(e))
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        output = error
    return output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=getenv("SERVER_PORT"),
                log_level="info", reload=True)
