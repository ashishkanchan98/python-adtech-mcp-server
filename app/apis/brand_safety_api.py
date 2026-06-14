def get_settings(line_item_id: str) -> dict:
    return {
        "lineItemId":           line_item_id,
        "brandSafetyTier":      "STANDARD",
        "verificationVendor":   "IAS",
        "blocklistDomains":     ["example-spam.com", "clickfarm.net"],
        "contentCategories":    ["ADULT", "VIOLENCE", "HATE_SPEECH"],
        "viewabilityThreshold": "50%",
    }


def get_placement_report(line_item_id: str, days: int) -> dict:
    return {
        "lineItemId":    line_item_id,
        "days":          days,
        "topDomains": [
            {"domain": "news.example.com",        "impressions": "45200", "ivtRate": "2.1%",  "brandSafeFlag": False},
            {"domain": "sport.example.com",        "impressions": "38100", "ivtRate": "1.8%",  "brandSafeFlag": False},
            {"domain": "traffic-exchange.xyz",     "impressions": "12400", "ivtRate": "41%",   "brandSafeFlag": True},
        ],
        "overallIvtRate": "4.3%",
    }
