from fastapi import APIRouter, HTTPException, Request
from services.github import GitHubService

router = APIRouter()
github_service = GitHubService()

@router.get("/analyze/{username}")
async def analyze_user(username: str, request: Request):
    try:
        data = await github_service.analyze_profile(username)
        if "error" in data:
            raise HTTPException(status_code=404, detail="User not found")
        return data
    except Exception as e:
        print(f"Error analyzing profile: {e}")
        raise HTTPException(status_code=500, detail=str(e))
