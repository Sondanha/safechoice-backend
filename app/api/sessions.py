from fastapi import APIRouter
from uuid import uuid4
from app.domain.scenario import DUMMY_SCENARIO
from app.service.scenario_engine import ScenarioEngine

router = APIRouter()
engine = ScenarioEngine(DUMMY_SCENARIO)

@router.post("/")
def create_session():
    session_id = str(uuid4())
    step = engine.get_initial_step()

    return {
        "session_id": session_id,
        "step": {
            "id": step["step_id"],
            "message": step["content"],
            "options": [
                {
                    "id": o["option_id"],
                    "label": o["label"],
                }
                for o in step.get("options", [])
            ],
        },
    }
