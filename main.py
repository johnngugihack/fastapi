from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import databases
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# MySQL database URL
DATABASE_URL = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
)

# Create database instance
database = databases.Database(DATABASE_URL)

# FastAPI app
app = FastAPI()

# Allow all CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic model for login
class UserCredentials(BaseModel):
    username: str
    password: str

@app.on_event("startup")
async def connect_db():
    await database.connect()

@app.on_event("shutdown")
async def disconnect_db():
    await database.disconnect()

@app.get("/")
async def read_root():
    return {"message": "FastAPI is running"}

@app.get("/hello/{name}")
async def log(name: str):
    return {"message": f"Welcome, {name}"}

@app.post("/login/")
async def login(credentials: UserCredentials):
    user_input = credentials.username

    # Query the database
    sql_query = "SELECT * FROM users WHERE username = :username"
    sql_values = {"username":user_input}
    user_data = await database.fetch_one(query=sql_query, values=sql_values)

    if user_data:
        return {
            "message": f"Welcome, {user_input}!"
        }
    else:
       user_pass=credentials.password
       sql_query = "INSERT INTO users (username,password) VALUES (:username, :password)"
       values = {"username": user_input, "password": user_pass}
       await database.execute(query=sql_query, values=values)
       return {
            "status" : "success"
        }
       
