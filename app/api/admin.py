from fastapi import APIRouter
from app.domain.scenario import SCENARIOS

router = APIRouter()

@router.get("/scenarios")
def list_scenarios():
    return [
        {
            "scenario_id": k,
            "title": v.get("meta", {}).get("title", ""),
            "triggers": v.get("meta", {}).get("triggers", []),
            "step_count": len(v.get("steps", [])),
        }
        for k, v in SCENARIOS.items()
    ]
