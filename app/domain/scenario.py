from typing import Dict, Any

SCENARIOS = {
    "bank_urgency": {
        "meta": {
            "title": "은행 사칭 · 긴급성",
            "triggers": ["urgency"]
        },
        "steps": [
            {
                "step_id": "step_1",
                "type": "message",
                "content": {"sender": "unknown", "text": "급한 연락입니다."},
                "options": [
                    {"option_id": "reply", "label": "응답", "next_step": "step_2"},
                    {"option_id": "ignore", "label": "무시", "next_step": "end_safe"}
                ]
            },
            {
                "step_id": "step_2",
                "type": "message",
                "content": {"sender": "system", "text": "지금 즉시 확인이 필요합니다."},
                "options": [
                    {"option_id": "proceed", "label": "확인", "next_step": "step_3"},
                    {"option_id": "stop", "label": "중단", "next_step": "end_safe"}
                ]
            }
        ]
    }
}

def load_scenario(scenario_id: str | None = None) -> Dict[str, Any]:
    if scenario_id and scenario_id in SCENARIOS:
        return SCENARIOS[scenario_id]
    return SCENARIOS["bank_urgency"]
