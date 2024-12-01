import base64
import json
import logging
from fastapi import FastAPI, HTTPException, Depends, Cookie, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List, Optional
import bcrypt
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import asynccontextmanager
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.middleware.cors import CORSMiddleware
import os
import cv2
import numpy as np
from dotenv import load_dotenv
from ml.module import Detector
load_dotenv()


DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@asynccontextmanager
async def lifespan(app: FastAPI):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL
                );
                CREATE TABLE IF NOT EXISTS files (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id),
                    file_name TEXT NOT NULL,
                    spore_class TEXT,
                    photo_base64 TEXT,
                    created_at TIMESTAMP DEFAULT NOW()
                );
            """)
            conn.commit()
        yield
    finally:
        conn.close()

app = FastAPI(lifespan=lifespan)


class AuthTokenMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user_id = request.cookies.get("user_id")
        if user_id:
            try:
                user_id = extract_user_id_from_token(user_id)
                
                request.state.user_id = user_id
            except Exception as e:
                raise HTTPException(status_code=400, detail="Invalid user_id")
        else:
            request.state.user_id = None
        response = await call_next(request)
        return response

def extract_user_id_from_token(token: str) -> int:
    if token.isdigit():
        return int(token)
    raise ValueError("Invalid token format")

app.add_middleware(AuthTokenMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], 
    allow_credentials=True,                
    allow_methods=["*"],                     
    allow_headers=["*"],                     
)

security = HTTPBasic()

class User(BaseModel):
    username: str
    password: str

class Base64Payload(BaseModel):
    data: str

class MultipleBase64Payload(BaseModel):
    data: List[str]

@app.post("/register/")
def register(user: User):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (user.username,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="User already exists")
            
            hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                (user.username, hashed_password.decode())
            )
            user_id = cur.fetchone()[0]
            conn.commit()

            response = JSONResponse(content={"id": user_id})
            return response
    finally:
        conn.close()

@app.post("/login/")
def login(credentials: HTTPBasicCredentials):
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT id, password FROM users WHERE username = %s", (credentials.username,))
            user = cur.fetchone()
            if not user or not bcrypt.checkpw(credentials.password.encode(), user["password"].encode()):
                raise HTTPException(status_code=401, detail="Invalid username or password")
            response = JSONResponse(content={"id": user["id"]})
            return response
    finally:
        conn.close()

def make_json_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    elif isinstance(obj, np.generic):
        return obj.item()
    elif isinstance(obj, dict):
        return {k: make_json_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_serializable(item) for item in obj]
    elif isinstance(obj, tuple):
        return tuple(make_json_serializable(item) for item in obj)
    else:
        return obj

@app.post("/process_base64/")
async def process_multiple_base64(payload: MultipleBase64Payload, user_id: Optional[str] = Cookie(None)):
    results = []
    if user_id:
        try:
            conn = get_db_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()

                if not user:
                    raise HTTPException(status_code=404, detail="User not found")

                for index, base64_data in enumerate(payload.data):
                    try:
                        detector = Detector()
                        img = process_base64_image(base64_data)
                        result = detector.work(img)
                        result["images"] = [cv2_to_base64(img) for img in result["images"]]
                        logging.debug(f"Result for index {index}: {result}")
                        result = make_json_serializable(result)
                        results.append(result)
                    except ValueError as e:
                        logging.error(f"Error processing image at index {index}: {e}")
                        results.append({"error": str(e), "index": index})
            return {"results": results}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            conn.close()
    else:
        for index, base64_data in enumerate(payload.data):
                    try:
                        detector = Detector()
                        img = process_base64_image(base64_data)
                        result = detector.work(img)
                        result["images"] = [cv2_to_base64(img) for img in result["images"]]
                        logging.debug(f"Result for index {index}: {result}")
                        result = make_json_serializable(result)
                        results.append(result)
                    except ValueError as e:
                        logging.error(f"Error processing image at index {index}: {e}")
                        results.append({"error": str(e), "index": index})
        return {"results": results}



@app.get("/user_history/")
async def get_user_history(user_id: Optional[str] = Cookie(None)):
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        conn = get_db_connection()
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(
                """
                SELECT id, file_name, spore_class, created_at 
                FROM files
                WHERE user_id = %s
                ORDER BY created_at DESC
                """,
                (user_id,)
            )
            records = cur.fetchall()

            if not records:
                return {"message": "No records found for this user."}

            return {"user_id": user_id, "history": records}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()


def process_base64_image(base64_string):
    try:
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        image_data = base64.b64decode(base64_string)

        np_array = np.frombuffer(image_data, np.uint8)

        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode image from base64 string.")

        return img

    except Exception as e:
        raise ValueError(f"Error processing base64 image: {e}")
    
def cv2_to_base64(img):
    _, buffer = cv2.imencode('.jpg', img)
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str