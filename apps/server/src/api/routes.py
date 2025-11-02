from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from config import MT4_EXPORT_FILE, TEMPLATES_DIR
from services.mt4_parser import parse_trade_data, extract_trade_info, filter_by_date_range

# Initialize templates
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

router = APIRouter()
api_router = APIRouter(prefix="/api")

# ==================== Web Routes (HTML) ====================

@router.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    """
    Serve the unified dashboard
    """
    try:
        return templates.TemplateResponse("index.html", {"request": request})
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Error loading dashboard"
            }
        )


# ==================== API Routes (JSON) ====================

@api_router.get("/summary")
async def get_summary(from_date: str = None, to_date: str = None):
    """
    Get trading summary with optional date range filtering.
    
    Args:
        from_date: Start date (format: 'YYYY.MM.DD')
        to_date: End date (format: 'YYYY.MM.DD')
        
    Returns:
        JSON object with summary statistics for the specified period
    """
    try:
        trade_data = parse_trade_data(str(MT4_EXPORT_FILE))
        
        if not trade_data:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": extract_trade_info([], from_date, to_date),
                    "message": "No trade data available"
                }
            )
        
        # Get summary with date range filtering
        summary = extract_trade_info(trade_data, from_date, to_date)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": summary
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Error retrieving trading summary"
            }
        )


@api_router.get("/trades")
async def get_trades(from_date: str = None, to_date: str = None):
    """
    Get all trades with optional date range filtering.
    
    Args:
        from_date: Start date (format: 'YYYY.MM.DD')
        to_date: End date (format: 'YYYY.MM.DD')
        
    Returns:
        JSON array of trades for the specified period
    """
    try:
        trade_data = parse_trade_data(str(MT4_EXPORT_FILE))
        
        if not trade_data:
            return JSONResponse(
                status_code=200,
                content={
                    "success": True,
                    "data": [],
                    "message": "No trade data available"
                }
            )
        
        # Filter by date range if provided
        if from_date or to_date:
            trade_data = filter_by_date_range(trade_data, from_date, to_date)
        
        # Separate trades from balance transactions
        trades = [t for t in trade_data if t.get('type') in ['buy', 'sell']]
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "data": trades,
                "count": len(trades)
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "message": "Error retrieving trades"
            }
        )


@api_router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    try:
        trade_data = parse_trade_data(str(MT4_EXPORT_FILE))
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "status": "healthy",
                "trades_count": len([t for t in trade_data if t.get('type') in ['buy', 'sell']]) if trade_data else 0
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "success": False,
                "status": "unhealthy",
                "error": str(e)
            }
        )
