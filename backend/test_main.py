from fastapi.testclient import TestClient
from fastapi import status
from dotenv import load_dotenv
from main import app
from os import getenv, remove
from os.path import getsize, exists, basename
from math import ceil
from faker import Faker
import random

load_dotenv()

client = TestClient(app)
file_store_path = getenv("LOG_PATH")
chunk_size = int(getenv("CHUNK_SIZE"))
fake = Faker()

def create_temporary_file():
    file_path = getenv("TEMPORARY_FILE_PATH") + "/" + fake.name().replace(" ", "-") + ".txt"

    with open(file_path, 'w') as file:
        for _ in range(random.randint(100,200)):
            name = fake.name()
            email = fake.email()
            phone = fake.phone_number()
            age = random.randint(18, 65)

            line = f"{name}, {email}, {phone}, {age}\n"
            file.write(line)

    return file_path

def delete_temporary_file(file_path):
    if exists(file_path):
        remove(file_path)

def delete_chunk_files(file_path, total_files):
    for i in range(total_files):
        chunk_file = f"{file_path}-{i}"
        if exists(chunk_file):
            remove(chunk_file)

def test_upload_chunk_file():
    file_path = create_temporary_file()
    file_name = basename(file_path)

    with open(file_path, "rb") as f:
        file_data = f.read()
    response = client.post(f"/upload/{file_name}",
                           headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", },
                           files={"data": file_data})
    assert response.status_code == status.HTTP_201_CREATED
    response_json = response.json()
    assert response_json['isSuccess'] == True

    delete_temporary_file(file_path)

def test_upload_full_file():
    file_path = create_temporary_file()
    file_name = basename(file_path)
    total_files = ceil(getsize(file_path) / chunk_size)
    i = 0
    with open(file_path, "rb") as in_file:
        chunk_file = in_file.read(chunk_size)
        while chunk_file:
            response = client.post(f"/upload/{file_name}-{i}",
                        headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", },
                        files={"data": chunk_file})
            assert response.status_code == status.HTTP_201_CREATED
            response_json = response.json()
            assert response_json['isSuccess'] == True
            chunk_file = in_file.read(chunk_size)
            i += 1

    if i == total_files:
        response = client.post("/upload/complete/", json={'file_unique_name': file_name})
        assert response.status_code == status.HTTP_201_CREATED

    delete_chunk_files(file_path, total_files)
    delete_temporary_file(file_path)

def test_upload_complete():
    payload = {"file_unique_name": "example_file_name.txt"}
    response = client.post("/upload/complete/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert "message" in data