from typing import List
from app.domain.event import Event
from app.domain.feature import Feature

class AnalysisEngine:
    @staticmethod
    def aggregate(events: List[Event]) -> Feature:
        f = Feature()

        if not events:
            return f

        events_sorted = sorted(events, key=lambda e: e.timestamp)

        # 반응 속도
        f.response_time_sec = (
            events_sorted[0].timestamp - events_sorted[0].timestamp
        ).total_seconds()

        # 단계 깊이
        f.max_step_reached = max(
            e.payload.get("step_index", 0) for e in events_sorted
        )

        # 트리거 반응
        for e in events_sorted:
            trigger = e.payload.get("trigger")
            if trigger:
                f.trigger_hits[trigger] = f.trigger_hits.get(trigger, 0) + 1

            if e.payload.get("verification") is True:
                f.verification_attempt += 1

        return f


    @staticmethod
    def score(feature: Feature) -> float:
        score = 0.0

        # 빠른 반응 = 위험
        if feature.response_time_sec < 5:
            score += 2.0

        # 깊이 들어갈수록 위험
        score += feature.max_step_reached * 1.0

        # 심리 트리거 반응
        score += feature.trigger_hits.get("urgency", 0) * 1.5
        score += feature.trigger_hits.get("authority", 0) * 1.5

        # 검증 시도는 감점
        score -= feature.verification_attempt * 2.0

        return max(round(score, 2), 0.0)

