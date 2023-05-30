from fastapi import FastAPI, File, UploadFile
import uvicorn
from sekop_log_parsing import log2html
from io import BytesIO

app = FastAPI()

@app.post("/upload/")
async def upload_file(file: UploadFile):

    with open('.log_name', 'wb') as f:
        log_name = f.write(file.file.read())

    return {"filesize": log_name}

@app.get("/track")
async def get_track(
        # log_file: str,
        start_time: str = None,
        end_time: str = None):


    map = log2html(
            '.log_name',
            start_time,
            end_time
            )

    return {"trackfile": map}

@app.get("/map")
async def get_map(file: UploadFile):

    txt = file.file.read()

    # Возврат имени файла карты
    return {"map": log2html(txt)}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, log_level="info")
