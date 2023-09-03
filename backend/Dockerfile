FROM python:3.10

WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app/
EXPOSE 80

# ENV FASTAPI_HOST ${SERVER_HOST}
# ENV FASTAPI_PORT ${SERVER_PORT}

RUN chmod +x setup.sh
RUN ./setup.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
