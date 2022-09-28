import { useState, useEffect } from "react";
import { ProgressBar, Form } from "react-bootstrap";

const chunkSize = 20;

function App() {
  const [counter, setCounter] = useState(0);
  const [chunkCount, setChunkCount] = useState(0);
  const [fileToBeUpload, setFileToBeUpload] = useState({});
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

  const getFileContext = (event) => {
    const file = event.target.files[0];
    console.log(file.type);
    console.log(file.name);
    setFileSize(file.size);

    const totalCount = Math.ceil(file.size / chunkSize);
    setChunkCount(totalCount);
    setFileToBeUpload(file);
    const uniqueName =
      Math.random().toString(36).slice(-6) + file.name.split(".").pop();
    setFileUniqueName(uniqueName);
  };

  const fileUpload = () => {
    setCounter(counter + 1);
    console.log(`${counter} and ${chunkCount} and ${fileSize}`);
    if (counter < chunkCount) {
      let chunk = fileToBeUpload.slice(chunkInitialByte, chunkFinishByte);
      uploadChunk(chunk);
    }
  };

  const uploadChunk = async (chunk) => {
    try {
      var formData = new FormData();
      console.log(chunk.type);


      formData.append(
        "file",
        chunk,
      );

      const response = await fetch(
        `http://localhost:8000/upload/${fileUniqueName}`,
        {
          method: "POST",
          headers: {
            "content-type": "application/octet-stream",
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
      if (counter === chunkCount) {
        console.log("Upload complete");
        await uploadCompleted();
      } else {
        let percentage = (counter / chunkCount) * 100;
        setProgress(percentage);
      }
    } catch (error) {
      console.log(error);
    }
  };

  const uploadCompleted = async () => {
    const response = await fetch("/upload/complete", {
      method: "POST",
      headers: {
        "content-type": "application/json",
      },
      body: {
        filename: fileUniqueName,
      },
    });
  };

  return (
    <Form.Group controlId="formFile" className="mb-3">
      <Form.Label>Upload Large File</Form.Label>
      <Form.Control type="file" onChange={getFileContext} />
    </Form.Group>
  );
}

export default App;
