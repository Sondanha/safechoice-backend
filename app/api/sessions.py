from fastapi import APIRouter
from uuid import uuid4
from app.domain.scenario import DUMMY_SCENARIO
from app.service.scenario_engine import ScenarioEngine

router = APIRouter()

engine = ScenarioEngine(DUMMY_SCENARIO)

@router.post("/")
def create_session():
    session_id = str(uuid4())
    first_step = engine.get_initial_step()

    return {
        "session_id": session_id,
        "step": {
            "step_id": first_step["step_id"],
            "type": first_step["type"],
            "content": first_step["content"],
            "options": [
                {"option_id": o["option_id"], "label": o["label"]}
                for o in first_step.get("options", [])
            ],
        }
    }
