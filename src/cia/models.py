from dataclasses import dataclass, field
from enum import StrEnum

type ModuleName = str
type ModuleSourceCode = str
type ModuleRuleName = str


class ModuleRuleOperation(StrEnum):
    ALLOWED = "allowed"
    NOT_ALLOWED = "not_allowed"


@dataclass
class ModuleRule:
    operation: ModuleRuleOperation
    imported_by: list[str]


@dataclass
class Rulebook:
    rules: dict[ModuleRuleName, ModuleRule]


@dataclass
class ImportStatement:
    module_name: ModuleName
    children: list[ModuleName]


@dataclass
class Module:
    name: ModuleName
    source_code: ModuleSourceCode
    import_statements: list[ImportStatement]


class AppliedRuleStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"


@dataclass
class AppliedRuleResult:
    rule: ModuleRule
    module: Module
    status: AppliedRuleStatus
