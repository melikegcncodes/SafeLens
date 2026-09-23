from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.analyzers.message_analyzer import analyze_message
from backend.analyzers.url_analyzer import analyze_urls
from backend.services.risk_engine import calculate_risk


app = FastAPI(
    title="SafeLens API",
    description="Phishing and scam detection API",
    version="0.4.0"
)
app.mount(
    "/static",
    StaticFiles(directory="frontend"),
    name="static"
)

class AnalysisRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return FileResponse("frontend/index.html")

@app.post("/analyze")
def analyze(request: AnalysisRequest):
    message_risks = analyze_message(request.message)
    url_risks = analyze_urls(request.message)

    detected_risks = message_risks + url_risks

    result = calculate_risk(detected_risks)

    return {
        "message": request.message,
        "risk_score": result["score"],
        "risk_level": result["level"],
        "detected_risks": detected_risks
    }