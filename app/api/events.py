from fastapi import APIRouter
from app.domain.event import Event
from app.domain.scenario import DUMMY_SCENARIO
from app.service.scenario_engine import ScenarioEngine

router = APIRouter()

# 지금은 더미 시나리오. DB 붙이면 교체

engine = ScenarioEngine(DUMMY_SCENARIO)

@router.post("/")
def collect_event(event: Event):
    next_step = engine.next_step(
        current_step_id=event.payload["current_step_id"],
        option_id=event.payload["option_id"],
    )

    if next_step["type"] == "end":
        return {"ended": True}

    return {
        "step": {
            "step_id": next_step["step_id"],
            "type": next_step["type"],
            "content": next_step["content"],
            "options": [
                {"option_id": o["option_id"], "label": o["label"]}
                for o in next_step.get("options", [])
            ],
        }
    }
