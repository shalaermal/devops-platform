from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string
import os

app = FastAPI(title="URL Shortener API")

# Database e thjeshtë në memory (PostgreSQL e shtojmë më vonë)
url_database = {}

class URLRequest(BaseModel):
    url: str

class URLResponse(BaseModel):
    short_code: str
    short_url: str
    original_url: str

def generate_code(length=6):
    """Gjeneron kod unik 6 karakteresh"""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@app.get("/health")
def health_check():
    """Kubernetes e përdor këtë për të kontrolluar nëse API punon"""
    return {"status": "healthy"}

@app.post("/shorten", response_model=URLResponse)
def shorten_url(request: URLRequest):
    """Merr URL të gjatë dhe kthen URL të shkurtuar"""
    # Gjenero kod unik
    code = generate_code()
    while code in url_database:
        code = generate_code()
    
    # Ruaj në database
    url_database[code] = {
        "original_url": request.url,
        "clicks": 0
    }
    
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    
    return URLResponse(
        short_code=code,
        short_url=f"{base_url}/{code}",
        original_url=request.url
    )

@app.get("/{code}")
def redirect_url(code: str):
    """Merr kodin e shkurtër dhe kthen URL origjinale"""
    if code not in url_database:
        raise HTTPException(status_code=404, detail="URL not found")
    
    url_database[code]["clicks"] += 1
    return {"original_url": url_database[code]["original_url"]}

@app.get("/stats/{code}")
def get_stats(code: str):
    """Kthen statistikat e një URL-je"""
    if code not in url_database:
        raise HTTPException(status_code=404, detail="URL not found")
    
    return {
        "code": code,
        "original_url": url_database[code]["original_url"],
        "clicks": url_database[code]["clicks"]
    }