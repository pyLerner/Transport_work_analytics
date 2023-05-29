from fastapi import FastAPI, File, UploadFile
import uvicorn
from sekop_log_parsing import log2html

app = FastAPI()

@app.post("/log")
async def put_log(
        file: UploadFile,
):
    return {"filename": file.file}

if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, log_level="info")