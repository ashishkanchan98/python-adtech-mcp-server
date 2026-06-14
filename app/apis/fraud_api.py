def get_click_log(campaign_id: str, hours: int) -> dict:
    return {
        "campaignId":       campaign_id,
        "lookbackHours":    hours,
        "totalClicks":      "4821",
        "suspiciousClicks": "1203",
        "suspiciousRate":   "24.9%",
        "topSuspiciousIps": ["185.220.101.x/24 (Tor exit)", "192.42.116.x/24 (VPN)"],
        "clickPatterns":    "Burst of 800 clicks in 3min window at 03:14 AM — bot signature",
    }


def get_ivt_report(campaign_id: str, vendor: str) -> dict:
    return {
        "campaignId":   campaign_id,
        "vendor":       vendor,
        "sivtRate":     "8.2%",
        "givtRate":     "3.1%",
        "totalIvtRate": "11.3%",
        "topFraudDomains": [
            {"domain": "traffic-exchange.xyz", "ivtRate": "41%"},
            {"domain": "click-network.biz",    "ivtRate": "28%"},
        ],
        "recommendation": "Block traffic-exchange.xyz and click-network.biz immediately",
    }
