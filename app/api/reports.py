from fastapi import APIRouter
from datetime import datetime, timedelta

from app.domain.event import Event, EventType
from app.service.analysis_engine import AnalysisEngine
from app.domain.report import Report
from app.service.feedback_engine import FeedbackEngine

router = APIRouter()  

@router.get("/{session_id}")
def get_report(session_id: str):
    dummy_events = [
        Event(
            session_id=session_id,
            type=EventType.CLICK,
            payload={"risk": "high"},
            timestamp=datetime.now() - timedelta(seconds=40)
        ),
        Event(
            session_id=session_id,
            type=EventType.INPUT,
            payload={"verification": True},
            timestamp=datetime.now()
        )
    ]

    feature = AnalysisEngine.aggregate(dummy_events)
    score = AnalysisEngine.score(feature)
    summary = FeedbackEngine.generate(feature, score)

    return Report(
        session_id=session_id,
        score=score,
        feature=feature,
        summary=summary
    )
