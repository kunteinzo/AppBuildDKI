from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt

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
def index():
    return jwt.encode(
        dict(
            uid=1000,
            exp=datetime.now(timezone.utc) + timedelta(minutes=2)
            ),
        "secret",
        algorithms="HS512"
    )


@app.post("/build")
def build(type: str, file: UploadFile, token: Annotated[dict, Depends(ck)]):
    return dict(msg=type, token=token, file_name=file.filename)
