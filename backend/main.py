from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.v1.endpoints import router as api_router

app = FastAPI(
    title="GitHub Profile Analyzer API",
    description="Backend for analyzing GitHub profiles with style.",
    version="1.0.0"
)

# CORS - Allow frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://*.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "GitHub Profile Analyzer API is Running"}
