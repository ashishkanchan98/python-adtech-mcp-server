def get_status(creative_id: str) -> dict:
    return {
        "creativeId":          creative_id,
        "reviewStatus":        "DISAPPROVED",
        "rejectionReasonCode": "POLICY_VIOLATION",
        "policyViolation":     "LANDING_PAGE_NOT_ACCESSIBLE",
        "detail":              "Click URL returned HTTP 404 during review crawl",
        "lastReviewed":        "2024-06-04T09:15:00Z",
        "resubmitEligible":    True,
    }


def get_asset(creative_id: str) -> dict:
    return {
        "creativeId":         creative_id,
        "format":             "DISPLAY",
        "dimensions":         "300x250",
        "fileSizeKb":         "148",
        "clickUrl":           "https://landing.example.com/offer-404",
        "declaredAttributes": ["HTTPS", "SSL_COMPLIANT"],
        "mimeType":           "image/jpeg",
    }
