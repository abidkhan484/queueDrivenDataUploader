import { useState, useEffect } from "react";
import { ProgressBar, Form } from "react-bootstrap";
import Button from "react-bootstrap/Button";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import "bootstrap/dist/css/bootstrap.css";

const chunkSize = process.env.REACT_APP_CHUNK_SIZE;
const apiEndoint = process.env.REACT_APP_API_ENDPOINT;
const apiPort = process.env.REACT_APP_API_PORT;

function App() {
  const [counter, setCounter] = useState(0);
  const [chunkCount, setChunkCount] = useState(0);
  const [fileToBeUpload, setFileToBeUpload] = useState({});
  const [fileObj, setFileObj] = useState({});
  const [fileUniqueName, setFileUniqueName] = useState("");
  const [fileSize, setFileSize] = useState(0);
  const [chunkInitialByte, setChunkInitialByte] = useState(0);
  const [chunkFinishByte, setChunkFinishByte] = useState(chunkSize);
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    if (fileSize > 0) {
      fileUpload();
    }
  }, [fileToBeUpload, progress]);

  const uploadFileObj = () => {
    setFileToBeUpload(fileObj);
  };

  const getFileContext = (event) => {
    const file = event.target.files[0];
    console.log(file.type);
    console.log(file.name);
    setFileSize(file.size);

    const totalCount = Math.ceil(file.size / chunkSize);
    setChunkCount(totalCount);
    setFileObj(file);
    const uniqueName = `${Math.random().toString(36).slice(-6)}-${file.name}`;
    setFileUniqueName(uniqueName);
  };

  const fileUpload = () => {
    setCounter(counter + 1);
    if (counter < chunkCount) {
      let chunk = fileToBeUpload.slice(chunkInitialByte, chunkFinishByte);
      uploadChunk(chunk);
    }
  };

  const uploadChunk = async (chunk) => {
    try {
      let formData = new FormData();

      formData.append("data", chunk);

      const response = await fetch(
        `${apiEndoint}:${apiPort}/upload/${fileUniqueName}-${counter - 1}`,
        {
          method: "POST",
          headers: {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "*",
          },
          body: formData,
        }
      );

      // const data = response.data;
      // add is success condition
      setChunkInitialByte(chunkFinishByte);
      setChunkFinishByte(chunkFinishByte + chunkSize);

      console.log(`${counter} and ${chunkCount} and ${fileSize}`);
      // make it more dev friendly
      if (counter + 1 === chunkCount) {
        console.log("Upload complete");
        await uploadCompleted();
        setProgress(100);
      } else {
        let percentage = (counter / chunkCount) * 100;
        setProgress(percentage);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const uploadCompleted = async () => {
    console.log(fileUniqueName);
    const response = await fetch(`${apiEndoint}:${apiPort}/upload/complete/`, {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: JSON.stringify({
        file_unique_name: fileUniqueName,
      }),
    });
    // show upload complete flash message according to the response
  };

  return (
    <div className="my-4">
      <Container>
        <div className="center">
          <Form.Group controlId="formFile" className="mb-3">
            <Form.Label>Upload Large File</Form.Label>
            <Form.Control type="file" onChange={getFileContext} />
            <Button variant="primary" onClick={uploadFileObj} className="mt-3">
              Upload
            </Button>
          </Form.Group>
        </div>
      </Container>
    </div>
  );
}

export default App;
