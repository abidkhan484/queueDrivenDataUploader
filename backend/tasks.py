from celery import Celery

app = Celery(
    'file_writing_task',
    broker='amqps://zzsfynmh:whMa8LaEmwo6-5ckfhAqrmqa47_jPNWc@armadillo.rmq.cloudamqp.com/zzsfynmh',
    # backend='amqp'
)


@app.task
def write_chunk_file(file_unique_name: str, chunk_content: bytes):
    file_store_path = f"logs/{file_unique_name}"
    with open(file_store_path, "wb") as f:
        f.write(chunk_content)
    
