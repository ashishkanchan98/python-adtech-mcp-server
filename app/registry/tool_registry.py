from dataclasses import dataclass


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    parameters_schema: str  # JSON string, lowercase types (OpenAI/LangChain compatible)


_TOOLS: list[ToolDefinition] = [

    # ── Campaign ──────────────────────────────────────────────────────────────
    ToolDefinition(
        "getCampaignStatus",
        "Fetch live status of a campaign: active/paused state, budget remaining, bid settings, audience size, and flight dates.",
        '{"type":"object","properties":{"campaignId":{"type":"string","description":"The campaign ID"},"advertiserId":{"type":"string","description":"Advertiser ID (optional, for scope)"}},"required":["campaignId"]}',
    ),
    ToolDefinition(
        "getCampaignFrequencySettings",
        "Returns frequency cap configuration at campaign and line item level.",
        '{"type":"object","properties":{"campaignId":{"type":"string"}},"required":["campaignId"]}',
    ),
    ToolDefinition(
        "getHourlySpendCurve",
        "Returns hourly spend breakdown over last N days to diagnose pacing issues.",
        '{"type":"object","properties":{"campaignId":{"type":"string"},"days":{"type":"integer","description":"Number of days to look back (default 3)"}},"required":["campaignId"]}',
    ),
    ToolDefinition(
        "getPacingSettings",
        "Returns pacing mode (ASAP, Even, Ahead) and daily budget settings for a campaign.",
        '{"type":"object","properties":{"campaignId":{"type":"string"}},"required":["campaignId"]}',
    ),
    ToolDefinition(
        "getPerformanceMetrics",
        "Returns ROAS, CTR, CPC, impressions, conversions for a campaign over a date range.",
        '{"type":"object","properties":{"campaignId":{"type":"string"},"dateRange":{"type":"string","description":"e.g. \'7d\', \'14d\', \'30d\'"}},"required":["campaignId","dateRange"]}',
    ),

    # ── Segment ───────────────────────────────────────────────────────────────
    ToolDefinition(
        "getSegmentStatus",
        "Returns processing state, size, and match rate of an audience segment.",
        '{"type":"object","properties":{"segmentId":{"type":"string"}},"required":["segmentId"]}',
    ),
    ToolDefinition(
        "getSegmentUploadLog",
        "Returns parse errors and rejection reasons from the last segment upload.",
        '{"type":"object","properties":{"segmentId":{"type":"string"}},"required":["segmentId"]}',
    ),

    # ── Creative ──────────────────────────────────────────────────────────────
    ToolDefinition(
        "getCreativeStatus",
        "Returns creative review status, rejection reason code, and policy violation details.",
        '{"type":"object","properties":{"creativeId":{"type":"string"}},"required":["creativeId"]}',
    ),
    ToolDefinition(
        "getCreativeAsset",
        "Returns creative metadata: dimensions, format, file size, click URL, declared attributes.",
        '{"type":"object","properties":{"creativeId":{"type":"string"}},"required":["creativeId"]}',
    ),

    # ── Pixel / Attribution ───────────────────────────────────────────────────
    ToolDefinition(
        "getPixelFireLog",
        "Returns pixel firing events: timestamps, user agents, IP ranges, event types.",
        '{"type":"object","properties":{"pixelId":{"type":"string"},"hours":{"type":"integer","description":"Look-back window in hours"}},"required":["pixelId"]}',
    ),
    ToolDefinition(
        "getAttributionWindowSettings",
        "Returns click-through and view-through attribution window settings for a campaign.",
        '{"type":"object","properties":{"campaignId":{"type":"string"}},"required":["campaignId"]}',
    ),
    ToolDefinition(
        "getConversionMatchRate",
        "Returns cookie/device ID match rate for attribution — key for diagnosing ITP/cookieless issues.",
        '{"type":"object","properties":{"pixelId":{"type":"string"}},"required":["pixelId"]}',
    ),

    # ── Brand Safety ──────────────────────────────────────────────────────────
    ToolDefinition(
        "getBrandSafetySettings",
        "Returns brand safety tier, blocklists, and third-party verification vendor settings for a line item.",
        '{"type":"object","properties":{"lineItemId":{"type":"string"}},"required":["lineItemId"]}',
    ),
    ToolDefinition(
        "getPlacementReport",
        "Returns top domains and apps where ads served, with IVT rates and brand safety flags.",
        '{"type":"object","properties":{"lineItemId":{"type":"string"},"days":{"type":"integer"}},"required":["lineItemId"]}',
    ),

    # ── PMP Deals ─────────────────────────────────────────────────────────────
    ToolDefinition(
        "getDealStatus",
        "Returns PMP deal sync state between DSP and SSP, including activation status.",
        '{"type":"object","properties":{"dealId":{"type":"string"}},"required":["dealId"]}',
    ),
    ToolDefinition(
        "getDealBidStream",
        "Returns bid request/response counts for a PMP deal over a time window.",
        '{"type":"object","properties":{"dealId":{"type":"string"},"hours":{"type":"integer"}},"required":["dealId"]}',
    ),
    ToolDefinition(
        "getSeatMapping",
        "Returns buyer seat ID configured on a deal and the DSP registered seat ID — critical for diagnosing zero-bid-request issues.",
        '{"type":"object","properties":{"dealId":{"type":"string"}},"required":["dealId"]}',
    ),

    # ── IVT / Fraud ───────────────────────────────────────────────────────────
    ToolDefinition(
        "getClickLog",
        "Returns click events with IP addresses, user agents, device IDs for fraud analysis.",
        '{"type":"object","properties":{"campaignId":{"type":"string"},"hours":{"type":"integer"}},"required":["campaignId"]}',
    ),
    ToolDefinition(
        "getIVTReport",
        'Calls IAS or DoubleVerify API to classify traffic as SIVT/GIVT and return fraud scores by domain.',
        '{"type":"object","properties":{"campaignId":{"type":"string"},"vendor":{"type":"string","enum":["IAS","DOUBLEVERIFY"]}},"required":["campaignId"]}',
    ),

    # ── Reporting Discrepancy ─────────────────────────────────────────────────
    ToolDefinition(
        "getDSPImpressionReport",
        "Returns impression counts from the DSP reporting API for a campaign and date range.",
        '{"type":"object","properties":{"campaignId":{"type":"string"},"startDate":{"type":"string"},"endDate":{"type":"string"}},"required":["campaignId","startDate","endDate"]}',
    ),
    ToolDefinition(
        "getGAMReport",
        "Queries Google Ad Manager API for impression/click data on a matching line item.",
        '{"type":"object","properties":{"lineItemId":{"type":"string"},"startDate":{"type":"string"},"endDate":{"type":"string"}},"required":["lineItemId","startDate","endDate"]}',
    ),
    ToolDefinition(
        "getDiscrepancyLog",
        "Returns historical DSP vs third-party impression discrepancy percentages for a campaign.",
        '{"type":"object","properties":{"campaignId":{"type":"string"}},"required":["campaignId"]}',
    ),

]


def get_all_tools() -> list[ToolDefinition]:
    return _TOOLS
