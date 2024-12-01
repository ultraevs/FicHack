import base64
import json
import logging
import os
from typing import List, Optional, Any, Dict

import bcrypt
import cv2
import numpy as np
import psycopg2
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Cookie,
    Request,
    Response,
)
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor
from starlette.middleware.base import BaseHTTPMiddleware

from ml.module import Detector

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# Database configuration using environment variables
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
}

def get_db_connection() -> psycopg2.extensions.connection:
    """
    Establishes a new database connection using the configuration.
    
    Returns:
        psycopg2.extensions.connection: A new database connection.
    """
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """
    Lifespan event handler to initialize database tables when the app starts.
    
    Args:
        app (FastAPI): The FastAPI application instance.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Create users and files tables if they do not exist
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
                    created_at TIMESTAMP DEFAULT NOW(),
                    time_taken TEXT NOT NULL,
                    avg_conf TEXT NOT NULL
                );
            """)
            conn.commit()
        yield
    finally:
        conn.close()

# Initialize FastAPI application with lifespan handler
app = FastAPI(lifespan=lifespan)

class AuthTokenMiddleware(BaseHTTPMiddleware):
    """
    Middleware to extract and validate the user_id from cookies and attach it to the request state.
    """
    async def dispatch(self, request: Request, call_next: Any) -> Response:
        user_id = request.cookies.get("user_id")
        if user_id:
            try:
                user_id_int = extract_user_id_from_token(user_id)
                request.state.user_id = user_id_int
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid user_id")
        else:
            request.state.user_id = None
        response = await call_next(request)
        return response

def extract_user_id_from_token(token: str) -> int:
    """
    Extracts the user ID from the provided token.
    
    Args:
        token (str): The token containing the user ID.
    
    Returns:
        int: The extracted user ID.
    
    Raises:
        ValueError: If the token format is invalid.
    """
    if token.isdigit():
        return int(token)
    raise ValueError("Invalid token format")

# Add custom authentication middleware
app.add_middleware(AuthTokenMiddleware)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize HTTP Basic authentication
security = HTTPBasic()

class User(BaseModel):
    """
    Pydantic model for user registration and login.
    """
    username: str
    password: str

class Base64Payload(BaseModel):
    """
    Pydantic model for single base64 encoded data.
    """
    data: str

class MultipleBase64Payload(BaseModel):
    """
    Pydantic model for multiple base64 encoded data with a file name.
    """
    file_name: str
    data: List[str]

@app.post("/register/")
def register(user: User) -> JSONResponse:
    """
    Endpoint to register a new user.
    
    Args:
        user (User): The user information containing username and password.
    
    Returns:
        JSONResponse: The response containing the newly created user ID.
    
    Raises:
        HTTPException: If the user already exists or a database error occurs.
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            # Check if the username already exists
            cur.execute("SELECT id FROM users WHERE username = %s", (user.username,))
            if cur.fetchone():
                raise HTTPException(status_code=400, detail="User already exists")
            
            # Hash the user's password
            hashed_password = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())

            # Insert the new user into the database
            cur.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s) RETURNING id",
                (user.username, hashed_password.decode())
            )
            user_id = cur.fetchone()[0]
            conn.commit()

            return JSONResponse(content={"id": user_id})
    finally:
        conn.close()

@app.post("/login/")
def login(credentials: HTTPBasicCredentials) -> JSONResponse:
    """
    Endpoint to authenticate a user and return their ID.
    
    Args:
        credentials (HTTPBasicCredentials): The user's login credentials.
    
    Returns:
        JSONResponse: The response containing the authenticated user ID.
    
    Raises:
        HTTPException: If authentication fails or a database error occurs.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Retrieve user information based on username
            cur.execute("SELECT id, password FROM users WHERE username = %s", (credentials.username,))
            user = cur.fetchone()
            if not user or not bcrypt.checkpw(credentials.password.encode(), user["password"].encode()):
                raise HTTPException(status_code=401, detail="Invalid username or password")
            
            return JSONResponse(content={"id": user["id"]})
    finally:
        conn.close()

def make_json_serializable(obj: Any) -> Any:
    """
    Recursively converts objects to a JSON-serializable format.
    
    Args:
        obj (Any): The object to convert.
    
    Returns:
        Any: The JSON-serializable object.
    """
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
async def process_multiple_base64(
    payload: MultipleBase64Payload,
    user_id: Optional[str] = Cookie(None)
) -> Dict[str, Any]:
    """
    Endpoint to process multiple base64-encoded images.
    
    Args:
        payload (MultipleBase64Payload): The payload containing file name and list of base64 data.
        user_id (Optional[str], optional): The user ID from cookies. Defaults to None.
    
    Returns:
        Dict[str, Any]: The results of processing each image.
    
    Raises:
        HTTPException: If a database error occurs.
    """
    results: List[Dict[str, Any]] = []
    conn: Optional[psycopg2.extensions.connection] = None

    if user_id:
        try:
            conn = get_db_connection()
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                # Verify that the user exists
                cur.execute("SELECT username FROM users WHERE id = %s", (user_id,))
                user = cur.fetchone()

                if not user:
                    raise HTTPException(status_code=404, detail="User not found")
                
                # Process each base64 image
                for index, base64_data in enumerate(payload.data):
                    try:
                        detector = Detector()
                        img = process_base64_image(base64_data)
                        result = detector.work(img)
                        result["images"] = [cv2_to_base64(image) for image in result["images"]]
                        logging.debug(f"Result for index {index}: {result}")
                        result_serializable = make_json_serializable(result)
                        print(result_serializable)

                        # Insert the processed file details into the database
                        cur.execute(
                            """
                            INSERT INTO files (
                                file_name, 
                                spore_class, 
                                photo_base64, 
                                created_at, 
                                user_id, 
                                time_taken, 
                                avg_conf
                            )
                            VALUES (%s, %s, %s, DEFAULT, %s, %s, %s)
                            """,
                            (
                                payload.file_name,
                                result["objects"],
                                json.dumps(result["images"]),
                                user_id,
                                result["time-taken"],
                                result["avg-conf"]
                            )
                        )
                        conn.commit()
                        results.append(result_serializable)
                    except ValueError as e:
                        logging.error(f"Error processing image at index {index}: {e}")
                        results.append({"error": str(e), "index": index})
            return {"results": results}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Database error: {e}")
        finally:
            if conn:
                conn.close()
    else:
        # Process images without user association
        for index, base64_data in enumerate(payload.data):
            try:
                detector = Detector()
                img = process_base64_image(base64_data)
                result = detector.work(img)
                result["images"] = [cv2_to_base64(image) for image in result["images"]]
                logging.debug(f"Result for index {index}: {result}")
                result_serializable = make_json_serializable(result)
                results.append(result_serializable)
            except ValueError as e:
                logging.error(f"Error processing image at index {index}: {e}")
                results.append({"error": str(e), "index": index})
        return {"results": results}

@app.get("/photo/{photo_id}/")
async def get_photo_details(photo_id: int) -> Dict[str, Any]:
    """
    Endpoint to retrieve details of a specific photo by its ID.
    
    Args:
        photo_id (int): The ID of the photo.
    
    Returns:
        Dict[str, Any]: The details of the photo.
    
    Raises:
        HTTPException: If the photo is not found or a database error occurs.
    """
    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Fetch photo details from the database
            cur.execute(
                """
                SELECT file_name, spore_class, photo_base64, avg_conf, time_taken
                FROM files
                WHERE id = %s
                """,
                (photo_id,)
            )
            record = cur.fetchone()

            if not record:
                raise HTTPException(status_code=404, detail="Photo not found")

            return {
                "file_name": record["file_name"],
                "spore_class": record["spore_class"],
                "photo_base64": record["photo_base64"],
                "avg_conf": record["avg_conf"],
                "time_taken": record["time_taken"],
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    finally:
        conn.close()

@app.get("/user_history/")
async def get_user_history(user_id: Optional[str] = Cookie(None)) -> Dict[str, Any]:
    """
    Endpoint to retrieve the history of processed files for a user.
    
    Args:
        user_id (Optional[str], optional): The user ID from cookies. Defaults to None.
    
    Returns:
        Dict[str, Any]: The user's processing history.
    
    Raises:
        HTTPException: If the user is not authenticated or a database error occurs.
    """
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")

    conn = get_db_connection()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            # Fetch user history from the database
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

def process_base64_image(base64_string: str) -> np.ndarray:
    """
    Decodes a base64-encoded string into an OpenCV image.
    
    Args:
        base64_string (str): The base64-encoded image string.
    
    Returns:
        np.ndarray: The decoded image.
    
    Raises:
        ValueError: If the image cannot be decoded.
    """
    try:
        # Remove data URL prefix if present
        if "," in base64_string:
            base64_string = base64_string.split(",")[1]

        # Decode the base64 string into bytes
        image_data = base64.b64decode(base64_string)

        # Convert bytes to a NumPy array
        np_array = np.frombuffer(image_data, np.uint8)

        # Decode the NumPy array into an image
        img = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if img is None:
            raise ValueError("Could not decode image from base64 string.")

        return img

    except Exception as e:
        raise ValueError(f"Error processing base64 image: {e}")

def cv2_to_base64(img: np.ndarray) -> str:
    """
    Encodes an OpenCV image to a base64 string.
    
    Args:
        img (np.ndarray): The image to encode.
    
    Returns:
        str: The base64-encoded image string.
    """
    # Encode the image as JPEG
    _, buffer = cv2.imencode('.jpg', img)
    # Convert to base64 string
    img_str = base64.b64encode(buffer).decode('utf-8')
    return img_str
