from pathlib import Path

from langchain_core.tools import tool

DATA_FILE = Path(__file__).parent / "company_data.md"


@tool
def lookup_company_policy(question: str) -> str:
    """
    Look up information from the company employee handbook.
    Use this tool for questions about leave policy, office timings,
    reimbursements, work from home, holidays, dress code,
    office locations, or IT support.
    """

    print("\n==============================")
    print("🔧 TOOL INVOKED")
    print(f"Question: {question}")
    print("==============================")

    return DATA_FILE.read_text(encoding="utf-8")