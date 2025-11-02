from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from services.mt4_parser import parse_trade_data
from services.data_analyzer import analyze_trade_data
from services.visualization import generate_visualizations
from config import MT4_EXPORT_FILE

router = APIRouter()

@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    trade_data = parse_trade_data(str(MT4_EXPORT_FILE))
    analysis_results = analyze_trade_data(trade_data)
    visualizations = generate_visualizations(analysis_results)
    return templates.TemplateResponse("dashboard.html", {"request": request, "visualizations": visualizations})