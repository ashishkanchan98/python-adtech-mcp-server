"""
Mock CampaignApiClient — hardcoded realistic responses identical to Java version.

Scenario routing by campaignId suffix:
  ends with 1  → PAUSED + budget exhausted + bid below floor + audience 0  (delivery failure)
  ends with 2  → ACTIVE + healthy budget + good bid                         (healthy campaign)
  ends with 3  → ACTIVE + budget ok + bid below floor                       (bid problem only)
  anything else→ PAUSED + budget exhausted (default bad state)
"""


def get_campaign_status(campaign_id: str) -> dict:
    if campaign_id and campaign_id.endswith("1"):
        return {
            "campaignId":       campaign_id,
            "status":           "PAUSED",
            "budgetRemaining":  "$0.00",
            "dailyBudget":      "$500.00",
            "bidFloor":         "$1.20",
            "currentBid":       "$0.95",
            "audienceSize":     "0",
            "flightStart":      "2024-05-01",
            "flightEnd":        "2024-07-30",
            "impressionsToday": "0",
            "issues": [
                "PAUSED — must be manually resumed",
                "Budget exhausted — $0.00 remaining of $500.00 daily",
                "Bid $0.95 is below floor $1.20 — will lose all auctions",
                "Audience size is 0 — segment upload may have failed",
            ],
        }
    if campaign_id and campaign_id.endswith("2"):
        return {
            "campaignId":       campaign_id,
            "status":           "ACTIVE",
            "budgetRemaining":  "$312.40",
            "dailyBudget":      "$500.00",
            "bidFloor":         "$1.10",
            "currentBid":       "$1.35",
            "audienceSize":     "142500",
            "flightStart":      "2024-05-01",
            "flightEnd":        "2024-07-30",
            "impressionsToday": "48320",
            "issues":           [],
        }
    if campaign_id and campaign_id.endswith("3"):
        return {
            "campaignId":       campaign_id,
            "status":           "ACTIVE",
            "budgetRemaining":  "$287.00",
            "dailyBudget":      "$500.00",
            "bidFloor":         "$2.50",
            "currentBid":       "$1.80",
            "audienceSize":     "98400",
            "flightStart":      "2024-05-01",
            "flightEnd":        "2024-07-30",
            "impressionsToday": "0",
            "issues": [
                "Bid $1.80 is $0.70 below floor $2.50 — winning zero auctions",
                "Raise bid to minimum $2.50 to start delivering",
            ],
        }
    return {
        "campaignId":       campaign_id or "UNKNOWN",
        "status":           "PAUSED",
        "budgetRemaining":  "$0.00",
        "dailyBudget":      "$500.00",
        "bidFloor":         "$1.20",
        "currentBid":       "$0.95",
        "audienceSize":     "0",
        "flightStart":      "2024-05-01",
        "flightEnd":        "2024-07-30",
        "impressionsToday": "0",
        "issues":           ["PAUSED — must be manually resumed", "Budget exhausted", "Bid below floor"],
    }


def get_frequency_settings(campaign_id: str) -> dict:
    return {
        "campaignId":              campaign_id,
        "campaignLevelCapEnabled": True,
        "campaignLevelCap":        "5 impressions per day",
        "lineItemCount":           4,
        "lineItemCap":             "5 impressions per day per line item",
        "effectiveMaxPerUser":     "20 per day (4 line items × 5)",
        "crossDeviceCapEnabled":   False,
        "warning": (
            "Campaign cap + line item caps are additive. "
            "A single user can see 20 ads/day. "
            "Recommend: remove campaign cap, keep line item cap at 2/day."
        ),
    }


def get_hourly_spend_curve(campaign_id: str, days: int) -> dict:
    return {
        "campaignId": campaign_id,
        "days":       days,
        "pacingMode": "ASAP",
        "dailyData": [
            {
                "date": "2024-06-03", "totalSpend": "$243.00", "budgetHit": False,
                "peakSpendHour": "09:00–10:00 AM ($68.00)", "afternoonSpend": "$82.00",
            },
            {
                "date": "2024-06-04", "totalSpend": "$198.00", "budgetHit": False,
                "peakSpendHour": "08:30–09:30 AM ($71.00)", "afternoonSpend": "$65.00",
            },
            {
                "date": "2024-06-05", "totalSpend": "$47.00", "budgetHit": True,
                "budgetHitTime": "08:03 AM",
                "peakSpendHour": "07:45–08:03 AM ($47.00)",
                "afternoonSpend": "$0.00 — budget exhausted",
            },
        ],
        "diagnosis": (
            "ASAP pacing front-loads spend into morning peak hours. "
            "Budget exhausted at 08:03 AM on Jun 5 — no delivery for remaining 16 hours."
        ),
        "fix": "Change pacing to EVEN to distribute $500 budget evenly across 24 hours (~$20.83/hr).",
    }


def get_pacing_settings(campaign_id: str) -> dict:
    return {
        "campaignId":     campaign_id,
        "pacingMode":     "ASAP",
        "dailyBudget":    "$500.00",
        "lifetimeBudget": "$15000.00",
        "budgetType":     "DAILY",
        "resetTime":      "00:00 UTC",
        "availableModes": ["ASAP", "EVEN", "AHEAD"],
        "recommendation": (
            "Switch from ASAP to EVEN. "
            "EVEN pacing targets $20.83/hr and prevents morning exhaustion."
        ),
    }


def get_performance_metrics(campaign_id: str, date_range: str) -> dict:
    return {
        "campaignId":   campaign_id,
        "dateRange":    date_range,
        "impressions":  "142500",
        "clicks":       "1283",
        "ctr":          "0.90%",
        "cpc":          "$0.82",
        "conversions":  "47",
        "cpa":          "$32.80",
        "roas":         "2.3x",
        "revenue":      "$3864.00",
        "spend":        "$1054.60",
        "avgFrequency": "3.2",
        "reachUnique":  "44531",
        "note": (
            "Metrics captured before delivery stopped on Jun 5 at 08:03 AM. "
            "Performance was strong — ROAS 2.3x above 2.0x target."
        ),
    }
