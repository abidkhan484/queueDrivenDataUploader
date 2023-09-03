Consider an application that offers users the capability to upload substantial volumes of data from the client side, sometimes reaching sizes as large as 1 GB. In such scenarios, it's critical to ensure that the user's experience remains smooth, without any interference from the data upload process.

The solution employs a clever approach to handle these colossal data uploads. It segments the data into manageable chunks and dispatches these chunks to a queue. Once dispatched, the application seamlessly orchestrates the merging of these data chunks, ensuring that the user is free to interact with the application without any disruptions.
## Installation

Copy `env.sample` to the `.env` and install the project with the below commands.

```bash
docker-compose up -d
```

To run the project without Docker, please consult the README files located within the respective frontend and backend directories for detailed instructions.
## Tech Stack

**Server:** FastAPI, Celery

**Client:** React, Bootstrap

## API Reference

It can be accessed through the FastAPI Swagger documentation, which is available at the [domain]/docs endpoint.


#### To store a chunk

```http
  POST /upload/{file_unique_name}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file_unique_name` | `string` | **Required**. Your file_unique_name |

The file_unique_name parameter should follow the format of adding file_name as a prefix and `-num` as a suffix, with num starting from 1. For example, it should look like `file_name.txt-1`.

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `data` | `string($binary)` | **Required**. Your data |

Header: `Content-Type: multipart/form-data`


#### To merge the chunks

```http
  POST /upload/complete
```

| Payload | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `file_unique_name` | `string` | **Required**. Your file_unique_name |

## Usage/Examples

The React-based frontend automatically submits data as soon as the file upload input is updated. It efficiently divides the files and transmits them to the server, adhering to the API specifications.

## Running Tests

To run tests for the backend, use the following command

```bash
  pytest
```

No UI test has been writen right now.
