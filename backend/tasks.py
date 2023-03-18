from celery import Celery
from dotenv import load_dotenv
from os import getenv

load_dotenv()

broker_url = getenv('BROKER_URL')

app = Celery(
    'file_writing_task',
    broker=broker_url,
    # backend='amqp'
)


@app.task
def write_chunk_file(file_unique_name: str, chunk_content: bytes):
    file_store_path = f"logs/{file_unique_name}"
    with open(file_store_path, "wb") as f:
        f.write(chunk_content)
    
