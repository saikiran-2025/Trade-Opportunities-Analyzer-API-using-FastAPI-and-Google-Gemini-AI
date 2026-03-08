from fastapi import APIRouter, Depends
from auth import create_token, verify_token
from data_scraper import get_market_news
from ai_analysis import get_available_models, analyze_market
from markdown_report import generate_report


router = APIRouter()


@router.get("/test")
async def test():
    return {"message": "Routes working!"}


@router.post("/login")
async def login(username: str):
    token = create_token(username)
    return {"token": token, "message": f"Welcome {username}!"}


@router.get("/protected")
async def protected_route(user=Depends(verify_token)):
    username = user.get("sub")
    return {"message": f"Hello {username}! This is protected content."}


@router.get("/news/{sector}")
async def get_news(sector: str, user=Depends(verify_token)):
    headlines = get_market_news(sector)
    return {
        "sector": sector,
        "headlines": headlines,
        "count": len(headlines),
    }


@router.get("/analyze/{sector}")
async def analyze_sector(sector: str, user=Depends(verify_token)):
    headlines = get_market_news(sector)
    analysis = analyze_market(sector, headlines)
    markdown = generate_report(sector, analysis)
    return {
        "sector": sector,
        "analysis": analysis,
        "markdown_report": markdown,
    }


@router.get("/models")
async def list_gemini_models():
    """
    Debug: show which Gemini models your API key can see.
    """
    models = get_available_models()
    return {"models": models}
