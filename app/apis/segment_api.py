def get_segment_status(segment_id: str) -> dict:
    return {
        "segmentId":            segment_id,
        "processingState":      "FAILED",
        "size":                 "0",
        "matchRate":            "0%",
        "lastUpload":           "2024-06-04T14:22:00Z",
        "errorSummary":         "Hash format validation failed — expected SHA-256 lowercase hex",
        "eligibleForTargeting": False,
    }


def get_upload_log(segment_id: str) -> dict:
    return {
        "segmentId":       segment_id,
        "totalRows":       "85000",
        "accepted":        "0",
        "rejected":        "85000",
        "rejectionReason": "INVALID_HASH_FORMAT",
        "detail":          "All hashes appear to be MD5 (32 chars). SHA-256 required (64 chars lowercase hex).",
        "lastAttempt":     "2024-06-04T14:22:00Z",
    }
