"""
Routes a tool name + args from the MCP client to the correct API module.
Python equivalent of Java ToolDispatcher.java — uses match statement (Python 3.10+).
"""
import logging

from app.apis import (
    brand_safety_api,
    campaign_api,
    creative_api,
    deal_api,
    fraud_api,
    pixel_api,
    reporting_api,
    segment_api,
)

logger = logging.getLogger(__name__)


def _str(args: dict, key: str) -> str | None:
    v = args.get(key)
    return str(v) if v is not None else None


def _str_or(args: dict, key: str, default: str) -> str:
    v = args.get(key)
    return str(v) if v is not None else default


def _int(args: dict, key: str, default: int) -> int:
    v = args.get(key)
    if isinstance(v, (int, float)):
        return int(v)
    return default


def dispatch(tool_name: str, args: dict) -> dict:
    logger.info("Dispatching tool=%s  args=%s", tool_name, args)

    match tool_name:

        # ── Campaign ──────────────────────────────────────────────────────
        case "getCampaignStatus":
            return campaign_api.get_campaign_status(_str(args, "campaignId"))
        case "getCampaignFrequencySettings":
            return campaign_api.get_frequency_settings(_str(args, "campaignId"))
        case "getHourlySpendCurve":
            return campaign_api.get_hourly_spend_curve(_str(args, "campaignId"), _int(args, "days", 3))
        case "getPacingSettings":
            return campaign_api.get_pacing_settings(_str(args, "campaignId"))
        case "getPerformanceMetrics":
            return campaign_api.get_performance_metrics(_str(args, "campaignId"), _str(args, "dateRange"))

        # ── Segment ───────────────────────────────────────────────────────
        case "getSegmentStatus":
            return segment_api.get_segment_status(_str(args, "segmentId"))
        case "getSegmentUploadLog":
            return segment_api.get_upload_log(_str(args, "segmentId"))

        # ── Creative ──────────────────────────────────────────────────────
        case "getCreativeStatus":
            return creative_api.get_status(_str(args, "creativeId"))
        case "getCreativeAsset":
            return creative_api.get_asset(_str(args, "creativeId"))

        # ── Pixel / Attribution ───────────────────────────────────────────
        case "getPixelFireLog":
            return pixel_api.get_fire_log(_str(args, "pixelId"), _int(args, "hours", 24))
        case "getAttributionWindowSettings":
            return pixel_api.get_attribution_window(_str(args, "campaignId"))
        case "getConversionMatchRate":
            return pixel_api.get_match_rate(_str(args, "pixelId"))

        # ── Brand Safety ──────────────────────────────────────────────────
        case "getBrandSafetySettings":
            return brand_safety_api.get_settings(_str(args, "lineItemId"))
        case "getPlacementReport":
            return brand_safety_api.get_placement_report(_str(args, "lineItemId"), _int(args, "days", 7))

        # ── PMP Deals ─────────────────────────────────────────────────────
        case "getDealStatus":
            return deal_api.get_deal_status(_str(args, "dealId"))
        case "getDealBidStream":
            return deal_api.get_bid_stream(_str(args, "dealId"), _int(args, "hours", 6))
        case "getSeatMapping":
            return deal_api.get_seat_mapping(_str(args, "dealId"))

        # ── IVT / Fraud ───────────────────────────────────────────────────
        case "getClickLog":
            return fraud_api.get_click_log(_str(args, "campaignId"), _int(args, "hours", 48))
        case "getIVTReport":
            return fraud_api.get_ivt_report(_str(args, "campaignId"), _str_or(args, "vendor", "IAS"))

        # ── Reporting ─────────────────────────────────────────────────────
        case "getDSPImpressionReport":
            return reporting_api.get_dsp_report(
                _str(args, "campaignId"), _str(args, "startDate"), _str(args, "endDate"))
        case "getGAMReport":
            return reporting_api.get_gam_report(
                _str(args, "lineItemId"), _str(args, "startDate"), _str(args, "endDate"))
        case "getDiscrepancyLog":
            return reporting_api.get_discrepancy_log(_str(args, "campaignId"))

        case _:
            logger.warning("Unknown tool requested: %s", tool_name)
            return {"error": f"Unknown tool: {tool_name}"}
