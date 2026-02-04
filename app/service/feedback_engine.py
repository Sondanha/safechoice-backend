from app.domain.feature import Feature

class FeedbackEngine:
    @staticmethod
    def generate(feature: Feature, score: float) -> str:
        reasons = []

        # 반응 속도
        if feature.response_time_sec < 5:
            reasons.append("메시지 수신 후 매우 빠르게 반응했습니다")

        # 단계 깊이
        if feature.max_step_reached >= 3:
            reasons.append("위험한 단계까지 진행했습니다")

        # 트리거
        if feature.trigger_hits.get("urgency", 0) > 0:
            reasons.append("긴급성 표현에 반응하는 경향이 보였습니다")
        if feature.trigger_hits.get("authority", 0) > 0:
            reasons.append("권위적 표현에 쉽게 흔들렸습니다")

        # 검증 시도
        if feature.verification_attempt == 0:
            reasons.append("발신자나 링크에 대한 검증 시도가 없었습니다")
        else:
            reasons.append("일부 검증 시도가 확인되었습니다")

        if not reasons:
            return "전반적으로 신중한 대응이 확인되었습니다"

        return " / ".join(reasons)
