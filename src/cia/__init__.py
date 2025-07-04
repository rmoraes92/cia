# import argparse as ap
import re
import ast
import tomllib
from logging import getLogger
from pathlib import Path

from .models import (
    ImportStatement,
    Module,
    ModuleName,
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
    rules = {}
    for rule in tomllib.loads(rule_file_body).get("rules", []):
        rules[rule["module"]] = ModuleRule(**rule)
    return Rulebook(rules=rules)


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
    module_file_path: Path, module_file_body: ModuleSourceCode
) -> Module:
    imports = parse_import_statements(module_file_body)
    module_name = module_file_path.name
    mod_abs_path = str(module_file_path).replace("/", ".")

    return Module(
        name=module_name,
        abs_path=mod_abs_path,
        source_code=module_file_body,
        import_statements=imports,
    )


def read_module_file(file_path: Path) -> ModuleSourceCode:
    with file_path.open() as f:
        return f.read()


def load_module(
    module_file_path: Path, module_file_body: ModuleSourceCode
) -> Module:

    return parse_module(module_file_path, module_file_body)


def apply_rulebook(
        importee_module: Module,
        rulebook: Rulebook
        ) -> list[AppliedRuleResult]:
    ret = []
    for import_statement in importee_module.import_statements:
        for abs_import_mod_path in import_statement.absolute_paths():
            for module_path_pattern, rule in rulebook.rules.items():
                if re.match(module_path_pattern, abs_import_mod_path):
                    for rule_importee_mod_pattern in rule.imported_by:
                        if re.match(rule_importee_mod_pattern, importee_module.abs_path):
                            if rule.modality == ModuleRuleOperation.ALLOWED:
                                ret.append(AppliedRuleResult(
                                    rule=rule,
                                    importee_module=importee_module,
                                    abs_imported_module_path=abs_import_mod_path,
                                    status=AppliedRuleStatus.PASSED
                                ))
                            elif rule.modality == ModuleRuleOperation.NOT_ALLOWED:
                                ret.append(AppliedRuleResult(
                                    rule=rule,
                                    importee_module=importee_module,
                                    abs_imported_module_path=abs_import_mod_path,
                                    status=AppliedRuleStatus.FAILED
                                ))
                            else:
                                logger.warning(f"module rule operation not implemented: {rule.modality.value}")

    return ret
