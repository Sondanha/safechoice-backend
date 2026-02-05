from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import sessions, events, reports

app = FastAPI(title="SAFECHOICE Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # MVP니까 정확히 이거
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(sessions.router, prefix="/sessions")
app.include_router(events.router, prefix="/events")
app.include_router(reports.router, prefix="/reports")

@app.get("/health")
def health():
    return {"status": "ok"}
