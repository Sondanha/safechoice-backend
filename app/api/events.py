from fastapi import APIRouter, HTTPException
from app.domain.event import Event
from app.service.scenario_engine import ScenarioEngine

router = APIRouter()

@router.post("/")
def collect_event(event: Event):
    # payload 안전 추출
    current_step_id = event.payload.get("current_step_id")
    option_id = event.payload.get("option_id")

    if not current_step_id or not option_id:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid payload: {event.payload}",
        )

    next_step = engine.next_step(
        current_step_id=current_step_id,
        option_id=option_id,
    )

    if next_step.get("type") == "end":
        return {"ended": True}

    return {
        "step": {
            "id": next_step["step_id"],       # 프론트 Step.id
            "message": next_step["content"],  # 프론트 message
            "options": [
                {
                    "id": o["option_id"],     # 프론트 option.id
                    "label": o["label"],
                }
                for o in next_step.get("options", [])
            ],
        }
    }
