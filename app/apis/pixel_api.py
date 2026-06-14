def get_fire_log(pixel_id: str, hours: int) -> dict:
    return {
        "pixelId":       pixel_id,
        "lookbackHours": hours,
        "totalFires":    "1847",
        "uniqueUsers":   "1203",
        "eventTypes":    {"purchase": 412, "add_to_cart": 893, "page_view": 542},
        "topUserAgents": ["Safari/17.0 (ITP active)", "Chrome/124", "Firefox/125"],
        "lastFire":      "2024-06-05T11:58:00Z",
    }


def get_attribution_window(campaign_id: str) -> dict:
    return {
        "campaignId":             campaign_id,
        "clickThroughWindowDays": "30",
        "viewThroughWindowDays":  "1",
        "attributionModel":       "LAST_CLICK",
        "note":                   "30-day click window may overcredit given ITP 7-day limit",
    }


def get_match_rate(pixel_id: str) -> dict:
    return {
        "pixelId":          pixel_id,
        "cookieMatchRate":  "14%",
        "deviceMatchRate":  "31%",
        "overallMatchRate": "18%",
        "itpImpact":        "HIGH",
        "safariFraction":   "52%",
        "recommendation":   "Match rate below 20% — ITP severely impacting attribution. Implement server-side tracking.",
    }
