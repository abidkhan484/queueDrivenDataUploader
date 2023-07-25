from fastapi.testclient import TestClient
from dotenv import load_dotenv
from main import app
from os import getenv, remove
from os.path import getsize, exists
from math import ceil
from faker import Faker
import random

load_dotenv()

client = TestClient(app)
file_store_path = getenv("LOG_PATH")
chunk_size = int(getenv("CHUNK_SIZE"))
fake = Faker()

def create_temporary_file():
    file_path = getenv("TEMPORARY_FILE_PATH") + "/" + fake.name() + ".txt"

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

def test_upload_chunk_file():
    file_path = create_temporary_file()
    fake_name = fake.name()

    with open(file_path, "rb") as f:
        file_data = f.read()
    response = client.post(f"/upload/{fake_name}",
                           headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", },
                           files={"data": file_data})
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['isSuccess'] == True

    delete_temporary_file(file_path)

def test_upload_full_file():
    file_path = create_temporary_file()
    fake_name = fake.name()
    total_files = ceil(getsize(file_path) / chunk_size)
    i = 0
    with open(file_path, "rb") as in_file:
        chunk_file = in_file.read(chunk_size)
        while chunk_file:
            response = client.post(f"/upload/{fake_name}-{i}",
                        headers={"Access-Control-Allow-Origin": "*", "Access-Control-Allow-Methods": "*", },
                        files={"data": chunk_file})
            assert response.status_code == 201
            response_json = response.json()
            assert response_json['isSuccess'] == True
            chunk_file = in_file.read(chunk_size)
            i += 1
    if i == total_files:
        response = client.post("/upload/complete", json={'file_unique_name': file_path})
        print(response.text)

    delete_temporary_file(file_path)
