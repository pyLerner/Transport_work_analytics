# WEB API для передачи в вэб приложение трека из лог файла по заданному временному интервалу

from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import FileResponse
import uvicorn
from sekop_log_parsing import log2html
from io import BytesIO
import random
import os
import time

app = FastAPI()

# Функция удаления закаченного файла через 5 минут
def remove_log(log_name: str) -> None:

    time.sleep(30)
    os.remove(log_name)

@app.post("/upload/")

async def upload_file(
        file: UploadFile,
        bg_task: BackgroundTasks
):

    # Случайный id номер
    id_session = str(random.randint(1000, 9999))
    log_name = '.' + id_session

    with open(log_name, 'wb') as f:
        log_file = f.write(file.file.read())

    # Фоновая задача для удаления файла через 5 минут
    bg_task.add_task(remove_log, log_name)

    return {"id": id_session,
            "filesize": log_file,
            "message": "LOG file will be deleted automatically after 5 minutes"
            }


# Построение трека по заданному временному интервалу
@app.get("/track")
async def get_track(
        bg_task: BackgroundTasks,
        id: str,
        start_time: str = None,
        end_time: str = None,

):

    log_name = '.' + id
    map_name = id + '.html'

    map = log2html(
            log_name,
            map_name,
            start_time,
            end_time
            )

    bg_task.add_task(remove_log, map_name)

    # return {"trackfile": map}

    return FileResponse(
        map,
        background=bg_task
    )


#Построение трека из файла целиком
@app.get("/map")
async def get_map(file: UploadFile):

    txt = file.file.read()

    # Возврат имени файла карты
    return {"map": log2html(txt)}


if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=5000, log_level="info")
