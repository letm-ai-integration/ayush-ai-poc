import ast

from pathlib import Path

from langchain_core.tools import tool
from logging_util import log_local_tool

# Ignore these folders while scanning
IGNORED_DIRS = {
    ".git",
    ".idea",
    ".vscode",
    "node_modules",
    "venv",
    ".venv",
    "__pycache__",
    "dist",
    "build",
    ".next",
    "coverage",
}

# Read only these file types
SUPPORTED_EXTENSIONS = {
    ".py",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".json",
    ".md",
    ".txt",
    ".yml",
    ".yaml",
    ".toml",
    ".html",
    ".css",
}


@tool
def analyze_project(project_path: str) ->str:
    """
    Analyze a software project.

    Returns only a concise overview of the project's
    structure and important source files.

    The returned information is intended to be sufficient
    for:
    - explaining the project
    - reviewing architecture
    - generating a short README
    """

    log_local_tool("analyze_project", project_path)

    BASE_DIRECTORY = Path(__file__).resolve().parent.parent.parent
    root = BASE_DIRECTORY / project_path

    if not root.exists():
        return f"Project '{project_path}' does not exist."

    if not root.is_dir():
        return f"'{project_path}' is not a directory."

    tree = []
    summaries = []

    for file in sorted(root.rglob("*")):

        if any(part in IGNORED_DIRS for part in file.parts):
            continue

        if not file.is_file():
            continue

        relative = file.relative_to(root)
        tree.append(str(relative))

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            text = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except Exception:
            continue

        imports = []
        classes = []
        functions = []

        if file.suffix == ".py":

            try:
                tree_ast = ast.parse(text)

                for node in tree_ast.body:

                    if isinstance(node, ast.Import):
                        imports.extend(
                            alias.name
                            for alias in node.names
                        )

                    elif isinstance(node, ast.ImportFrom):
                        if node.module:
                            imports.append(node.module)

                    elif isinstance(node, ast.ClassDef):
                        classes.append(node.name)

                    elif isinstance(node, ast.FunctionDef):
                        functions.append(node.name)

            except Exception:
                pass

        summaries.append(
            f"""
FILE: {relative}

Imports:
{", ".join(imports[:5]) or "None"}

Classes:
{", ".join(classes[:5]) or "None"}

Functions:
{", ".join(functions[:10]) or "None"}
"""
        )

    return f"""
PROJECT NAME
{root.name}

PROJECT PATH
{root}

==================================================

DIRECTORY STRUCTURE

{chr(10).join(tree[:80])}

==================================================

SOURCE FILE OVERVIEW

{chr(10).join(summaries)}

==================================================

IMPORTANT:

The information above is sufficient to understand the
project and generate a SHORT README.

If asked to generate a README:

- Keep it under 25 lines.
- Include:
  * Project title
  * One paragraph overview
  * Directory structure
  * Main technologies
  * How to run (only if obvious)
- Do NOT invent features.
- Do NOT create long sections.
- Do NOT add Future Work, License, Contributing,
  Acknowledgements or placeholders unless they are
  clearly present in the project.
"""


@tool
def write_file(file_path: str, content: str) -> str:
    """
    Write text content to a file.

    Use this tool ONLY when the user explicitly requests creating or
    modifying a file.

    The content should be concise and reasonably sized.
    Avoid writing excessively large documents unless explicitly requested.
    """

    log_local_tool("write_file", file_path)

    BASE_DIRECTORY = Path(__file__).resolve().parent.parent.parent
    path = BASE_DIRECTORY / file_path

    path.parent.mkdir(parents=True, exist_ok=True)

    path.write_text(
        content,
        encoding="utf-8"
    )

    return f"Successfully wrote file:\n{file_path}"