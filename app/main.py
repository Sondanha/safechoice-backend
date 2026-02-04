from fastapi import FastAPI
from app.api import sessions, events, reports

app = FastAPI(title="SAFECHOICE Backend")

app.include_router(sessions.router, prefix="/sessions")
app.include_router(events.router, prefix="/events")
app.include_router(reports.router, prefix="/reports")

@app.get("/health")
def health():
    return {"status": "ok"}
