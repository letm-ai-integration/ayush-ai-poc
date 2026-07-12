from state import TripState


def fan_out_research(state: TripState) -> list[str]:
    return ["flight_finder", "accommodation_scout", "activity_planner", "weather_advisor"]


def route_after_budget(state: TripState) -> str:
    breakdown = state.get("budget_breakdown") or {}
    if not breakdown.get("is_over_budget"):
        return "approved"

    total = breakdown.get("total_estimated", 0)
    budget = state["preferences"].get("budget_usd", 1) if state.get("preferences") else 1
    overage_pct = (total - budget) / budget if budget else 0
    return "needs_human_review" if overage_pct > 0.20 else "approved"


def route_after_budget_review(state: TripState) -> str:
    if state.get("budget_approved"):
        return "approved"
    if state.get("iteration_count", 0) >= 2:
        return "approved"
    return "optimize"
