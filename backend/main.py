from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class Base64Payload(BaseModel):
    data: str

@app.post("/v1/process/")
async def process_base64(payload: Base64Payload):
    try:
        return {"received_data": payload.data}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))