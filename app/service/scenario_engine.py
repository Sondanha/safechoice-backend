from typing import Dict, Any

class ScenarioEngine:
    def __init__(self, scenario: Dict[str, Any]):
        self.steps = {s["step_id"]: s for s in scenario["steps"]}

    def get_initial_step(self) -> Dict[str, Any]:
        # 첫 step은 배열 첫 원소로 가정
        return list(self.steps.values())[0]

    def next_step(self, current_step_id: str, option_id: str) -> Dict[str, Any]:
        step = self.steps[current_step_id]
        for opt in step.get("options", []):
            if opt["option_id"] == option_id:
                next_id = opt["next_step"]
                if next_id.startswith("end"):
                    return {"type": "end", "step_id": next_id}
                return self.steps[next_id]
        raise ValueError("Invalid option")
