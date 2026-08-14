import json
import sqlite3
import uuid
from datetime import datetime

from database.repository import connect


def new_code() -> str:
    """Tạo mã hồ sơ duy nhất, kể cả khi người dùng bấm nhiều lần trong cùng một giây."""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = uuid.uuid4().hex[:8].upper()
    return f"HS-DEMO-{timestamp}-{random_suffix}"


def create_application(user_id, payload, result, fee) -> str:
    """Lưu hồ sơ và tự thử lại nếu xảy ra va chạm mã hồ sơ."""
    last_error = None

    for _ in range(5):
        code = new_code()
        try:
            with connect() as connection:
                connection.execute(
                    """
                    INSERT INTO applications(
                        application_code,
                        applicant_user_id,
                        asset_id,
                        applicant_name,
                        phone_number,
                        purpose_code,
                        requested_area_m2,
                        start_date,
                        end_date,
                        description,
                        has_image,
                        status,
                        submitted_at,
                        ai_result_json,
                        fee_amount
                    )
                    VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        code,
                        user_id,
                        payload["asset_id"],
                        payload["applicant_name"],
                        payload["phone_number"],
                        payload["purpose_code"],
                        payload["requested_area_m2"],
                        payload["start_date"].isoformat(),
                        payload["end_date"].isoformat(),
                        payload.get("description", ""),
                        int(payload.get("has_image", False)),
                        "DANG_KIEM_TRA",
                        datetime.now().isoformat(timespec="seconds"),
                        json.dumps(result, ensure_ascii=False),
                        fee["total_amount"],
                    ),
                )
                connection.commit()
            return code
        except sqlite3.IntegrityError as exc:
            last_error = exc
            if "applications.application_code" not in str(exc):
                raise

    raise RuntimeError(
        "Không thể tạo mã hồ sơ duy nhất sau nhiều lần thử."
    ) from last_error


def list_applications():
    with connect() as connection:
        rows = connection.execute(
            """
            SELECT a.*, s.asset_code, s.asset_name, u.username
            FROM applications a
            JOIN assets s ON s.id = a.asset_id
            JOIN users u ON u.id = a.applicant_user_id
            ORDER BY a.id DESC
            """
        ).fetchall()
    return [dict(row) for row in rows]


def update_status(code, status, note):
    permit = "GP-" + code.replace("HS-", "") if status == "DA_CHAP_THUAN" else None
    with connect() as connection:
        connection.execute(
            """
            UPDATE applications
            SET status = ?,
                officer_note = ?,
                permit_code = COALESCE(?, permit_code)
            WHERE application_code = ?
            """,
            (status, note, permit, code),
        )
        connection.commit()
    return permit
