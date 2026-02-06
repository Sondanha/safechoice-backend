from fastapi import APIRouter
from uuid import uuid4
from typing import Optional

from app.domain.scenario import load_scenario
from app.service.scenario_engine import ScenarioEngine

router = APIRouter()

@router.post("/")
def create_session(scenario_id: Optional[str] = None):
    session_id = str(uuid4())

    scenario = load_scenario(scenario_id)
    engine = ScenarioEngine(scenario)

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
