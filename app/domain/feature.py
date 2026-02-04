from pydantic import BaseModel
from typing import List, Dict, Optional

class Feature(BaseModel):
    response_time_sec: float = 0.0          # 첫 이벤트까지 걸린 시간
    max_step_reached: int = 0                # 단계 깊이
    trigger_hits: Dict[str, int] = {}        # urgency, authority 등
    verification_attempt: int = 0            # 검증 시도 횟수
