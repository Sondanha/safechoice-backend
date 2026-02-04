DUMMY_SCENARIO = {
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
