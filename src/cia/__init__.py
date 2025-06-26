import argparse as ap
import ast
import os
import tomllib
from dataclasses import dataclass, field
from enum import StrEnum
from logging import getLogger
from pathlib import Path

from .models import (ImportStatement, Module, ModuleRuleName, ModuleSourceCode,
                     Rulebook)

logger = getLogger(__name__)


def read_rulebook_file(file_path: Path) -> str:
    with file_path.open() as f:
        return f.read()


def load_rulebook(rule_file_body: str) -> Rulebook:
    rules_dict = tomllib.loads(rule_file_body)
    return Rulebook(rules=rules_dict)


def parse_import_statements(
    module_file_body: ModuleSourceCode,
) -> list[ImportStatement]:
    tree: ast.Module = ast.parse(module_file_body)

    import_statements: list[ImportStatement] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_statements.append(ImportStatement(root=alias.name, children=[]))
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module if node.module else "(relative import)"
            children = []

            for alias in node.names:
                children.append(alias.name)

            import_statements.append(
                ImportStatement(root=module_name, children=children)
            )

    return import_statements


def parse_module(
    module_name: ModuleRuleName, module_file_body: ModuleSourceCode
) -> Module:
    imports = parse_import_statements(module_file_body)

    return Module(
        name=module_name,
        source_code=module_file_body,
        import_statements=imports,
    )


def read_module_file(file_path: Path) -> ModuleSourceCode:
    with file_path.open() as f:
        return f.read()


def load_module(module_file_path: Path, module_file_body: ModuleSourceCode) -> Module:
    module_name = module_file_path.name
    return parse_module(module_name, module_file_body)
