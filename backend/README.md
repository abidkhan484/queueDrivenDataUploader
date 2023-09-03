The `Dockerfile` can be used to create a container as described in the root README. For development purposes, you can also run the project independently.
## Installation

Copy `env.sample` to the `.env` and install the project with the below commands.

Create and activate a new virtual enviornment

```sh
python -m venv env && source env/bin/activate
```

Install the dependencies

```sh
pip install -r requirements.txt
```

Initial setup
```sh
bash setup.sh
```

Start the server

```sh
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Start celery in log mode

```sh
celery -A tasks.app worker --loglevel=INFO
```

To run test with detail view, use the below command
```sh
pytest -s
```


## Tech Stack
- React
- Bootstrap
