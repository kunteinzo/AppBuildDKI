from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import subprocess
import os

HOME = os.getenv("HOME")
PJ_DIR = HOME+"/PJ"
APK_PATH = "/app/build/outputs/apk/"

def check():
    if not os.path.exists(PJ_DIR):
        os.mkdir(PJ_DIR)


def cmd(cmd: list|str):
    return subprocess.run(
        cmd,
        capture_output=True, text=True
    )


app = FastAPI()
oauth = OAuth2PasswordBearer(tokenUrl="token")

async def ck(token: Annotated[str, Depends(oauth)]):
    try:
        return jwt.decode(
            token,
            "secret",
            algorithms=["HS512"]
        )
    except Exception as e:
        raise HTTPException(401, str(e))


@app.get("/thekey")
def index(is_dev: int = 0):
    return dict(token=jwt.encode(
        dict(
            uid=1000,
            exp=datetime.now(timezone.utc) + timedelta(minutes=(60 if is_dev == 1 else 2))
            ),
        "secret",
        algorithm="HS512"
    ))


@app.post("/build")
def build(type: str, file: UploadFile, token: Annotated[dict, Depends(ck)]):
    return dict(msg=type, token=token, file_name=file.filename)


@app.post("/uploadBuild")
def upload_build(file: UploadFile, token: Annotated[dict, Depends(ck)]):
    check()
    with open(f"{PJ_DIR}/{file.filename}", "wb") as f:
        while len(b:=file.file.read(1024)) > 0:
            f.write(b)
    res = cmd(["unzip", "-o", "-K", f"{HOME}/{file.filename}", "-d", f"{PJ_DIR}"])
    PJD = f"{PJ_DIR}/{file.filename[:-4]}"
    cmd(["chmod", "+x", f"{PJD}/gradlew"])
    #cmd(["cd", PJD, "&&", "./gradlew", "assemble"])
    zip_name = f"{file.filename[:-4]}.zip",
    cmd(["cd", PJD, "&&", "zip", "-r", zip_name, "*"])
    return FileResponse(PJD+'/'+zip_name)
