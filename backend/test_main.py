from fastapi.testclient import TestClient
from dotenv import load_dotenv
from main import app
from os import getenv
from os.path import getsize
from math import ceil


load_dotenv()

client = TestClient(app)
file_store_path = getenv("LOG_PATH")
chunk_size = int(getenv("CHUNK_SIZE"))

def test_upload_chunk_file():
    with open("/home/polymath/Downloads/sequence.txt", "rb") as f:
        file = f.read()
    response = client.post("/upload/abowfhn",
                           headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", },
                           files={"data": file})
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['isSuccess'] == True

def test_upload_full_file():
    filename = "/home/polymath/Downloads/epc_error.txt"
    total_files = ceil(getsize(filename) / chunk_size)
    i = 0
    with open(filename, "rb") as in_file:
        chunk_file = in_file.read(chunk_size)
        while chunk_file:
            response = client.post(f"/upload/abowfhn-{i}",
                        headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", },
                        files={"data": chunk_file})
            print(response.text)
            assert response.status_code == 201
            response_json = response.json()
            assert response_json['isSuccess'] == True
            chunk_file = in_file.read(chunk_size)
            i += 1
    if i == total_files:
         client.post(f"/upload/complete", json={'file_unique_name': filename})
