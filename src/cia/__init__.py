import ast
import os
import tomllib
import argparse as ap
from dataclasses import dataclass
from pathlib import Path
from logging import getLogger

type ModuleName = str
type ModuleSourceCode = str

logger = getLogger(__name__)

@dataclass
class ImportStatement:
    root: ModuleName
    children: list[ModuleName]


def parse_import_statements(tree: ast.AST) -> list[ImportStatement]:
    """
    Parses import statements from the given module source code.

    Args:
        module_src (ModuleSourceCode): The source code of the module.

    Returns:
        list[ImportStatement]: A list of import statements found in the module.
    """
    import_statements = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_statements.append(
                    ImportStatement(root=alias.name)
                )
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module if node.module else "(relative import)"
            children = []

            for alias in node.names:
                children.append(alias.name)

            import_statements.append(
                ImportStatement(root=module_name, children=children)
            )

    return import_statements

def read_rules_file(file_path: Path) -> str:
    with file_path.open() as f:
        return f.read()

def load_rules(rule_file_body: str) -> dict:
    return tomllib.loads(rule_file_body)


def read_

def analyze_imports(cfg_file_path: Path, module_file_path: Path):
    with cfg_file_path.open("r") as f:
        cfg = tomllib.load(f)

    with module_file_path.open("r", encoding="utf-8") as f:
        module_source_code: ModuleSourceCode = f.read()

    try:
        tree = ast.parse(module_source_code)
    except SyntaxError as e:
        logger.error(f"Error parsing script '{module_file_path}': {e}")
        return

    import_lists = parse_import_statements(tree)

    if not import_lists:
        logger.info("  No import statements found in this script.")
        return

    for import_statement in import_lists:
        if import_statement.children:
            logger.info(f"  Import: {import_statement.root} -> {', '.join(import_statement.children)}")
        else:
            logger.info(f"  Import: {import_statement.root} (no children)")


def main():
    p = ap.ArgumentParser(
        description="Core Import Analyzer"
    )
    p.add_argument("-r", "--rules", help="Path to the toml file containing the import flow rules")
    p.add_argument("script", help="Path to a Folder or  a Python script to analyze")
    args = p.parse_args()

    analyze_imports(args.script)

if __name__ == "__main__":
    main()
    # --- Example Usage ---
    # Create a dummy Python script for testing
    # Analyze the dummy script
    #analyze_imports(dummy_script_name)
