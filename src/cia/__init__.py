# import argparse as ap

import ast
import tomllib
from logging import getLogger
from pathlib import Path

from .models import (
    ImportStatement,
    Module,
    ModuleRuleName,
    ModuleSourceCode,
    Rulebook,
    ModuleRule,
    ModuleRuleOperation,
    AppliedRuleResult,
    AppliedRuleStatus,
)

logger = getLogger(__name__)


def read_rulebook_file(file_path: Path) -> str:
    with file_path.open() as f:
        return f.read()


def load_rulebook(rule_file_body: str) -> Rulebook:
    rules_dict = tomllib.loads(rule_file_body)
    for module_name, rule_dict in rules_dict.items():
        rules_dict[module_name] =  ModuleRule(**rule_dict)

    return Rulebook(rules=rules_dict)


def parse_import_statements(
    module_file_body: ModuleSourceCode,
) -> list[ImportStatement]:
    tree: ast.Module = ast.parse(module_file_body)

    import_statements: list[ImportStatement] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                import_statements.append(
                    ImportStatement(module_name=alias.name, children=[])
                )
        elif isinstance(node, ast.ImportFrom):
            module_name = node.module if node.module else "(relative import)"
            children = []

            for alias in node.names:
                children.append(alias.name)

            import_statements.append(
                ImportStatement(module_name=module_name, children=children)
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


def load_module(
    module_file_path: Path, module_file_body: ModuleSourceCode
) -> Module:
    module_name = module_file_path.name
    return parse_module(module_name, module_file_body)


def apply_rulebook(module: Module, rulebook: Rulebook) -> list[AppliedRuleResult]:
    ret = []
    for import_statement in module.import_statements:
        module_rule = rulebook.rules.get(import_statement.module_name)

        if module_rule is None:
            continue

        if module_rule.operation == ModuleRuleOperation.NOT_ALLOWED \
            and module.name in module_rule.imported_by:
                ret.append(AppliedRuleResult(
                    module=module,
                    rule=module_rule,
                    status=AppliedRuleStatus.FAILED,
                ))

    return ret
