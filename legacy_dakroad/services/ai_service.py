from __future__ import annotations
from typing import Any

def fallback_assessment(rule_result: dict, application: dict) -> dict:
    triggered = rule_result.get("rule_results", [])
    missing = [r["message"] for r in triggered if r["rule_id"] in {"R01","R05","R10"}]
    warnings = [r["message"] for r in triggered if r["status"] == "REVIEW"]
    checklist = []
    if any(r["rule_id"] == "R03" for r in triggered):
        checklist.append("Kiểm tra thực địa phạm vi và diện tích đề nghị.")
    if any(r["rule_id"] == "R09" for r in triggered):
        checklist.append("Đánh giá ảnh hưởng đến an toàn giao thông.")
    if any(r["rule_id"] == "R11" for r in triggered):
        checklist.append("Đối chiếu mục đích sử dụng với cấu hình vị trí.")
    if not checklist:
        checklist.append("Đối chiếu hồ sơ gốc và xác nhận thông tin trước khi xử lý.")

    return {
        "mode": "FALLBACK_RULE_BASED",
        "summary": (
            f"Hồ sơ đề nghị sử dụng {application.get('requested_area_m2', 0)} m² "
            f"cho mục đích {application.get('purpose_code', '')}."
        ),
        "overall_status": rule_result.get("overall_status", "CAN_BO_XEM_XET"),
        "missing_items": missing,
        "warnings": warnings,
        "triggered_rules": [r["rule_id"] for r in triggered],
        "recommended_action": rule_result.get("recommended_action", "Cán bộ xem xét."),
        "officer_checklist": checklist,
        "disclaimer": "Kết quả hỗ trợ tự động, không thay thế việc thẩm định và quyết định của người có thẩm quyền."
    }

def assess_application(rule_result: dict, application: dict) -> dict:
    # MVP v0.2 mặc định dùng chế độ dự phòng minh bạch, không phụ thuộc API.
    # Có thể thay thế phần này bằng lời gọi API trong phiên bản sau.
    return fallback_assessment(rule_result, application)
