from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# import databases
import os
# from dotenv import load_dotenv

# Load environment variables
# load_dotenv()

# MySQL database URL
# DATABASE_URL = (
#     f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
#     f"@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
# )

# Create database instance
# database = databases.Database(DATABASE_URL)

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
    # await database.connect()
    pass

@app.on_event("shutdown")
async def disconnect_db():
    # await database.disconnect()
    pass

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
    sql_values = {"username": user_input}
    # user_data = await database.fetch_one(query=sql_query, values=sql_values)

    if False:  # Replace with: if user_data:
        return {
            "message": f"Welcome, {user_input}!"
        }
    else:
        user_pass = credentials.password
        sql_query = "INSERT INTO users (username, password) VALUES (:username, :password)"
        values = {"username": user_input, "password": user_pass}
        # await database.execute(query=sql_query, values=values)
        return {
            "status": "success"
        }

@app.get("/status")
def get_status():
    response = {
        "currentState": {
            "result": "completed"
        },
        "qualifications": [
            {
                "id": "complete-profile",
                "title": "Create profile",
                "status": "qualified",
                "description": "unlocks Playground"
            },
            {
                "id": "skill-selection",
                "title": "Import skills",
                "status": "qualified",
                "description": "matches you with projects"
            },
            {
                "id": "identity",
                "title": "Verify identity",
                "status": "qualified"
            },
            {
                "id": "skill-screenings",
                "title": "Verify skills",
                "status": "qualified",
                "description": "unlocks your first project",
                "disallowMobile": True
            }
        ]
    }
    from fastapi.responses import JSONResponse
    return JSONResponse(content=response)
