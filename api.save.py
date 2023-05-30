from fastapi import FastAPI, UploadFile
import uvicorn
from sekop_log_parsing import log2html

app = FastAPI()


@app.post("/log")
async def put_log(
        file: UploadFile,
):

    txt = file.file.read()

    # Раскомментировать, если нужен plain text
    # return {"file": file.file.read()}

    # Возврат имени файла карты
    return {"map": log2html(txt)}

@app.get("/map")
async def get_map():
    return None


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, log_level="info")