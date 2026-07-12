import os
from rich.console import Console
from rich.table import Table

from config import settings
from graph import build_travel_graph
from visualize import save_graph_visuals

if settings.tracing_enabled:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
    os.environ["LANGCHAIN_API_KEY"] = settings.langsmith_api_key

console = Console()


def display_destinations(options: list[dict]) -> None:
    table = Table(title="Destination Options")
    table.add_column("#")
    table.add_column("Name")
    table.add_column("Country")
    table.add_column("Match Score")
    for i, opt in enumerate(options, start=1):
        table.add_row(str(i), opt.get("name", ""), opt.get("country", ""), str(opt.get("match_score", "")))
    console.print(table)


def main():
    app = build_travel_graph()
    save_graph_visuals(app)

    config = {"configurable": {"thread_id": "trip-001"}}
    user_input = console.input("[bold cyan]Describe your trip:[/] ")

    state = app.invoke(
        {
            "user_input": user_input,
            "iteration_count": 0,
            "error_messages": [],
            "destination_options": [],
            "flight_options": [],
            "hotel_options": [],
            "activities": [],
            "status": "start",
        },
        config,
    )

    display_destinations(state["destination_options"])
    choice = int(console.input("Select destination (1-3): ")) - 1
    app.update_state(config, {"selected_destination": state["destination_options"][choice]["name"]})
    state = app.invoke(None, config)

    snapshot = app.get_state(config)
    if "human_approve_budget" in snapshot.next:
        console.print(state["budget_breakdown"])
        approve = console.input("Over budget — approve anyway? (y/n): ").lower() == "y"
        app.update_state(config, {"budget_approved": approve, "iteration_count": state["iteration_count"] + 1})
        state = app.invoke(None, config)

    console.print(state["final_itinerary"])

    os.makedirs("outputs", exist_ok=True)
    with open("outputs/itinerary.md", "w", encoding="utf-8") as f:
        f.write(str(state["final_itinerary"]))
    console.print("[green]Saved outputs/itinerary.md[/]")


if __name__ == "__main__":
    main()
