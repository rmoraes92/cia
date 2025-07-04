from dataclasses import dataclass, field
from enum import StrEnum
from types import ModuleType

type ModuleName = str
type ModuleSourceCode = str
type ModulePathRegex = str
type ModuleAbsPath = str

class ModuleRuleOperation(StrEnum):
    ALLOWED = "allowed"
    NOT_ALLOWED = "not_allowed"


@dataclass
class ModuleRule:
    module: ModulePathRegex
    modality: ModuleRuleOperation
    imported_by: list[str]


@dataclass
class Rulebook:
    rules: dict[ModulePathRegex, ModuleRule]


@dataclass
class ImportStatement:
    module_name: ModuleName
    children: list[ModuleName]

    def absolute_paths(self) -> list[str]:
        ret = []

        for c in self.children:
            ret.append(f"{self.module_name}.{c}")

        if not ret:
            ret.append(self.module_name)

        return ret


@dataclass
class Module:
    name: ModuleName
    abs_path: ModuleAbsPath
    source_code: ModuleSourceCode
    import_statements: list[ImportStatement]


class AppliedRuleStatus(StrEnum):
    PASSED = "passed"
    FAILED = "failed"

@dataclass
class AppliedRuleResult:
    rule: ModuleRule
    importee_module: Module
    abs_imported_module_path: ModuleAbsPath
    status: AppliedRuleStatus
