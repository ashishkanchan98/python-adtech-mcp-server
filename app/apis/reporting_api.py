def get_dsp_report(campaign_id: str, start_date: str, end_date: str) -> dict:
    return {
        "campaignId":     campaign_id,
        "startDate":      start_date,
        "endDate":        end_date,
        "dspImpressions": "1284500",
        "dspClicks":      "11562",
        "dspSpend":       "$1540.20",
    }


def get_gam_report(line_item_id: str, start_date: str, end_date: str) -> dict:
    return {
        "lineItemId":     line_item_id,
        "startDate":      start_date,
        "endDate":        end_date,
        "gamImpressions": "1197300",
        "gamClicks":      "10804",
        "discrepancy":    "6.8%",
        "note":           "6.8% discrepancy within acceptable 10% threshold. Likely due to measurement timing differences.",
    }


def get_discrepancy_log(campaign_id: str) -> dict:
    return {
        "campaignId": campaign_id,
        "historicalDiscrepancies": [
            {"date": "2024-06-01", "dsp": "420000", "thirdParty": "391000", "pct": "6.9%"},
            {"date": "2024-06-02", "dsp": "398000", "thirdParty": "371000", "pct": "6.8%"},
            {"date": "2024-06-03", "dsp": "466500", "thirdParty": "435000", "pct": "6.7%"},
        ],
        "avgDiscrepancy": "6.8%",
        "threshold":      "10%",
        "status":         "WITHIN_ACCEPTABLE_RANGE",
    }
