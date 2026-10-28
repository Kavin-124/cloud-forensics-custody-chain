import os
import json
from datetime import datetime

AUDIT_LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "audit_logs.json")
DISPUTES_FILE = os.path.join(os.path.dirname(__file__), "..", "disputes.json")

def get_audit_logs() -> list:
    if not os.path.exists(AUDIT_LOG_FILE):
        return []
    try:
        with open(AUDIT_LOG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def log_event(actor_name: str, actor_role: str, action: str, details: str, status: str = "SUCCESS"):
    logs = get_audit_logs()
    entry = {
        "log_id": f"LOG-{len(logs) + 1:04d}",
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "actor": actor_name,
        "role": actor_role.upper(),
        "action": action,
        "details": details,
        "status": status
    }
    logs.append(entry)
    with open(AUDIT_LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)
    return entry

def get_disputes() -> list:
    if not os.path.exists(DISPUTES_FILE):
        return []
    try:
        with open(DISPUTES_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def lodge_dispute(lawyer_user: dict, case_id: str, block_id: int, reason: str, legal_ground: str) -> tuple[bool, str]:
    disputes = get_disputes()
    dispute_id = f"DSP-{datetime.utcnow().year}-{len(disputes) + 101}"
    entry = {
        "dispute_id": dispute_id,
        "case_id": case_id,
        "block_id": block_id,
        "filed_by": lawyer_user.get("full_name"),
        "bar_id": lawyer_user.get("identifier"),
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
        "reason": reason,
        "legal_ground": legal_ground,
        "status": "PENDING_JUDICIAL_REVIEW",
        "ruling": None,
        "ruled_by": None,
        "ruling_timestamp": None
    }
    disputes.append(entry)
    with open(DISPUTES_FILE, "w", encoding="utf-8") as f:
        json.dump(disputes, f, indent=4)
    log_event(lawyer_user.get("full_name"), "LAWYER", "LODGE_DISPUTE", f"Filed {dispute_id} against Case {case_id} Block #{block_id}")
    return True, f"Dispute {dispute_id} lodged successfully and forwarded to the Judicial Bench."

def record_judicial_ruling(judge_user: dict, dispute_id: str, ruling: str, comments: str) -> tuple[bool, str]:
    disputes = get_disputes()
    target = None
    for d in disputes:
        if d.get("dispute_id") == dispute_id:
            target = d
            break
    if not target:
        return False, "Dispute not found."
    target["status"] = ruling # e.g. "OBJECTION_SUSTAINED" (Rejected) or "OBJECTION_OVERRULED" (Admitted)
    target["ruling"] = comments
    target["ruled_by"] = judge_user.get("full_name")
    target["ruling_timestamp"] = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(DISPUTES_FILE, "w", encoding="utf-8") as f:
        json.dump(disputes, f, indent=4)
    log_event(judge_user.get("full_name"), "JUDGE", "JUDICIAL_RULING", f"Issued ruling '{ruling}' on {dispute_id}")
    return True, f"Judicial Order recorded for {dispute_id}."
