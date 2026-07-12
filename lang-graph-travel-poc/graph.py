from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

from agents import (
    preference_parser_node,
    destination_researcher_node,
    human_select_destination_node,
    flight_finder_node,
    accommodation_scout_node,
    activity_planner_node,
    weather_advisor_node,
    budget_calculator_node,
    human_approve_budget_node,
    itinerary_compiler_node,
)
from edges import fan_out_research, route_after_budget, route_after_budget_review
from state import TripState


def build_travel_graph():
    graph = StateGraph(TripState)

    graph.add_node("preference_parser", preference_parser_node)
    graph.add_node("destination_researcher", destination_researcher_node)
    graph.add_node("human_select_destination", human_select_destination_node)
    graph.add_node("flight_finder", flight_finder_node)
    graph.add_node("accommodation_scout", accommodation_scout_node)
    graph.add_node("activity_planner", activity_planner_node)
    graph.add_node("weather_advisor", weather_advisor_node)
    graph.add_node("budget_calculator", budget_calculator_node)
    graph.add_node("human_approve_budget", human_approve_budget_node)
    graph.add_node("itinerary_compiler", itinerary_compiler_node)

    graph.add_edge(START, "preference_parser")
    graph.add_edge("preference_parser", "destination_researcher")
    graph.add_edge("destination_researcher", "human_select_destination")

    graph.add_conditional_edges(
        "human_select_destination",
        fan_out_research,
        ["flight_finder", "accommodation_scout", "activity_planner", "weather_advisor"],
    )

    graph.add_edge("flight_finder", "budget_calculator")
    graph.add_edge("accommodation_scout", "budget_calculator")
    graph.add_edge("activity_planner", "budget_calculator")
    graph.add_edge("weather_advisor", "budget_calculator")

    graph.add_conditional_edges(
        "budget_calculator",
        route_after_budget,
        {"approved": "itinerary_compiler", "needs_human_review": "human_approve_budget"},
    )
    graph.add_conditional_edges(
        "human_approve_budget",
        route_after_budget_review,
        {"approved": "itinerary_compiler", "optimize": "activity_planner"},
    )

    graph.add_edge("itinerary_compiler", END)

    memory = MemorySaver()
    return graph.compile(
        checkpointer=memory,
        interrupt_before=["human_select_destination", "human_approve_budget"],
    )
