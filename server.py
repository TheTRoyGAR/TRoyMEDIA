"""
TRoyMEDIA Agent Execution Server
Exposes CrewAI agents as REST endpoints.
Run with: python server.py
"""

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import logging
import os
import hmac
import threading
import httpx
from dotenv import load_dotenv
from agency import TRoyMEDIAAgency
from agency.core.memory import shared_memory

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="TRoyMEDIA Agent Server",
    description="Execute CrewAI agents and return results",
    version="1.0.0"
)

BACKEND_API_KEY = os.getenv("BACKEND_API_KEY", "")


@app.on_event("shutdown")
def _drain_shared_memory():
    shared_memory.close()


@app.middleware("http")
async def require_backend_key(request: Request, call_next):
    if request.url.path in ("/health", "/docs", "/openapi.json", "/redoc"):
        return await call_next(request)

    if not BACKEND_API_KEY:
        logger.warning("BACKEND_API_KEY is not set — refusing all non-health requests.")
        return JSONResponse(status_code=503, content={"detail": "Server not configured: BACKEND_API_KEY missing"})

    provided = request.headers.get("x-backend-key", "")
    if not hmac.compare_digest(provided, BACKEND_API_KEY):
        return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

    return await call_next(request)


agency = TRoyMEDIAAgency()


class TaskRequest(BaseModel):
    task_id: str
    brief: str
    department: str = ""
    skill: str = ""
    callback_url: str = ""


class TaskResponse(BaseModel):
    task_id: str
    status: str
    result: str


@app.get("/health")
def health_check():
    return {"status": "online", "service": "TRoyMEDIA Agent Executor", "agency_version": "1.0.0"}


@app.get("/status")
def status():
    return agency.status()


@app.get("/memory/records")
def memory_records(limit: int = 100):
    records = shared_memory.list_records()
    records.sort(key=lambda r: r.created_at, reverse=True)
    return {
        "count": len(records),
        "records": [
            {
                "id": r.id,
                "scope": r.scope,
                "categories": r.categories,
                "content": r.content,
                "importance": r.importance,
                "created_at": r.created_at.isoformat() if hasattr(r.created_at, "isoformat") else str(r.created_at),
            }
            for r in records[:limit]
        ],
    }


def _run_and_callback(task_id: str, department: str, skill: str, brief: str, callback_url: str) -> None:
    try:
        result = route_and_execute(department, skill, brief)
        payload = {"status": "completed", "output": result}
        logger.info(f"Task {task_id} completed successfully")
    except Exception as e:
        logger.error(f"Task {task_id} failed: {str(e)}")
        payload = {"status": "failed", "output": str(e)}

    try:
        httpx.post(callback_url, json=payload, headers={"X-Backend-Key": BACKEND_API_KEY}, timeout=30)
    except Exception as e:
        logger.error(f"Task {task_id}: callback to {callback_url} failed: {str(e)}")


@app.post("/execute", response_model=TaskResponse)
def execute_task(request: TaskRequest) -> TaskResponse:
    if request.callback_url:
        thread = threading.Thread(
            target=_run_and_callback,
            args=(request.task_id, request.department, request.skill, request.brief, request.callback_url),
            daemon=True,
        )
        thread.start()
        return TaskResponse(task_id=request.task_id, status="accepted", result="")

    try:
        result = route_and_execute(request.department, request.skill, request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/orchestrate", response_model=TaskResponse)
def orchestrate_brief(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.intake_brief(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/marketing/trend-scrape", response_model=TaskResponse)
def marketing_trend_scrape(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.marketing.trend_scrape(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/marketing/content-gen", response_model=TaskResponse)
def marketing_content_gen(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.marketing.content_gen(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/marketing/publicity-audit", response_model=TaskResponse)
def marketing_publicity_audit(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.marketing.publicity_audit(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sales/pitch-development", response_model=TaskResponse)
def sales_pitch_development(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.sales.pitch_development(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sales/distribution-deal", response_model=TaskResponse)
def sales_distribution_deal(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.sales.distribution_deal(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/sales/objection-handler", response_model=TaskResponse)
def sales_objection_handler(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.sales.objection_handler(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/finance/production-budget", response_model=TaskResponse)
def finance_production_budget(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.finance.production_budget(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/finance/royalty-tracking", response_model=TaskResponse)
def finance_royalty_tracking(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.finance.royalty_tracking(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/finance/reporting", response_model=TaskResponse)
def finance_reporting(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.finance.reporting(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/production/casting-call", response_model=TaskResponse)
def production_casting_call(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.production.casting_call(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/production/production-schedule", response_model=TaskResponse)
def production_production_schedule(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.production.production_schedule(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/production/talent-support", response_model=TaskResponse)
def production_talent_support(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.production.talent_support(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/production/script-development", response_model=TaskResponse)
def production_script_development(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.production.script_development(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/production/crew-support", response_model=TaskResponse)
def production_crew_support(request: TaskRequest) -> TaskResponse:
    try:
        result = agency.production.crew_support(request.brief)
        return TaskResponse(task_id=request.task_id, status="completed", result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


def route_and_execute(department: str, skill: str, brief: str) -> str:
    department = department.lower()
    skill = skill.lower()

    routes = {
        "orchestrator": {
            "intake_brief": agency.intake_brief,
        },
        "production": {
            "daily_briefing": agency.run_daily_briefing,
            "casting_call": agency.production.casting_call,
            "production_schedule": agency.production.production_schedule,
            "talent_support": agency.production.talent_support,
            "script_development": agency.production.script_development,
            "crew_support": agency.production.crew_support,
            "run_task": agency.production.run_task,
        },
        "marketing": {
            "trend_scrape": agency.marketing.trend_scrape,
            "content_gen": agency.marketing.content_gen,
            "publicity_audit": agency.marketing.publicity_audit,
            "run_campaign": agency.marketing.run_campaign,
        },
        "sales": {
            "pitch_development": agency.sales.pitch_development,
            "distribution_deal": agency.sales.distribution_deal,
            "objection_handler": agency.sales.objection_handler,
            "run_pipeline": agency.sales.run_pipeline,
        },
        "finance": {
            "production_budget": agency.finance.production_budget,
            "royalty_tracking": agency.finance.royalty_tracking,
            "reporting": agency.finance.reporting,
            "generate_report": agency.finance.generate_report,
        },
    }

    handler = routes.get(department, {}).get(skill)
    if handler is None:
        raise ValueError(f"Unknown department/skill: {department}/{skill}")
    return handler(brief)


if __name__ == "__main__":
    import sys
    import uvicorn

    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8")

    print("========================================================")
    print("       TRoyMEDIA Agent Execution Server")
    print("       Starting at http://localhost:8200")
    print("       API docs at http://localhost:8200/docs")
    print("========================================================")

    uvicorn.run(app, host="0.0.0.0", port=8200, log_level="info")
