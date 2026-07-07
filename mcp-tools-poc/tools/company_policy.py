from pathlib import Path

from langchain_core.tools import tool

from logging_util import log_local_tool

DATA_FILE = Path(__file__).resolve().parent.parent / "company_data.md"


@tool
def lookup_company_policy(question: str) -> str:
    """
    Look up information from the company employee handbook.
    Use this tool for questions about leave policy, office timings,
    reimbursements, work from home, holidays, dress code,
    office locations, or IT support.
    """

    log_local_tool("lookup_company_policy", question)

    return DATA_FILE.read_text(encoding="utf-8")