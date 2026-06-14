def get_deal_status(deal_id: str) -> dict:
    return {
        "dealId":                    deal_id,
        "dealType":                  "PMP",
        "sspActivationStatus":       "ACTIVE",
        "dspActivationStatus":       "ACTIVE",
        "flightStart":               "2024-06-01",
        "flightEnd":                 "2024-07-31",
        "fixedPrice":                "$4.50 CPM",
        "estimatedDailyImpressions": "500000",
    }


def get_bid_stream(deal_id: str, hours: int) -> dict:
    return {
        "dealId":              deal_id,
        "lookbackHours":       hours,
        "bidRequestsReceived": "0",
        "bidResponsesSent":    "0",
        "winRate":             "N/A",
        "note":                "Zero bid requests indicate seat ID mismatch or deal not propagated to DSP",
    }


def get_seat_mapping(deal_id: str) -> dict:
    return {
        "dealId":              deal_id,
        "buyerSeatIdOnDeal":   "seat-adtech-001",
        "dspRegisteredSeatId": "ADTECH-001",
        "mismatchDetected":    True,
        "detail":              "Case mismatch: SSP has 'seat-adtech-001', DSP registered as 'ADTECH-001'. SSP is case-sensitive.",
    }
