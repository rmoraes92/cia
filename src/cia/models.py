from dataclasses import dataclass, field
from enum import StrEnum
from logging import getLogger

type ModuleName = str
type ModuleSourceCode = str
type ModuleRuleName = str


class ModuleRuleOperation(StrEnum):
    ALLOWED = "allowed"
    NOT_ALLOWED = "not_allowed"


@dataclass
class ModuleRule:
    operation: ModuleRuleOperation
    imported_by: list[str] | None = None
    import_from: list[str] | None = None


@dataclass
class Rulebook:
    rules: dict[ModuleRuleName, ModuleRule] = field(default_factory=dict)


@dataclass
class ImportStatement:
    root: ModuleName
    children: list[ModuleName]


@dataclass
class Module:
    name: ModuleName
    source_code: ModuleSourceCode
    import_statements: list[ImportStatement]
