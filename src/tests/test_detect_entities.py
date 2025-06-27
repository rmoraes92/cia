import unittest
from pathlib import Path

import cia

"""
Rework the TOML format to:
[module_a]
operation = "allowed"
imported_by = ["module_d"]

[module_d]
operation = "allowed"
import_from = ["module_a"]
"""


class ParsingRulebookTestCase(unittest.TestCase):

    def test_parsing_with_dataclasses(self):
        rule_file_body = """
        [module_a]
        operation = "allowed"
        imported_by = ["module_d"]
        """
        rules = cia.load_rulebook(
            rule_file_body,
        )
        self.assertTrue(isinstance(rules, cia.Rulebook))
        self.assertTrue(len(rules.rules) == 1)


class ParsingPythonModuleTestCase(unittest.TestCase):

    def test_parsing_import_statements(self):
        python_mod_body = (
            "import a\n" "def hello_world():\n" "    print('Hello, World!')\n"
        )

        imports = cia.parse_import_statements(python_mod_body)

        self.assertTrue(len(imports) == 1)
        self.assertTrue(imports[0].module_name == "a")

        python_mod_body = (
            "from a import func_a\n"
            "def hello_world():\n"
            "    print('Hello, World!')\n"
        )

        imports = cia.parse_import_statements(python_mod_body)

        self.assertTrue(len(imports) == 1)
        self.assertTrue(imports[0].module_name == "a")
        self.assertTrue(len(imports[0].children) == 1)
        self.assertTrue(imports[0].children[0] == "func_a")


class ApplyingRulesTestCase(unittest.TestCase):

    def _build_rulebook(self) -> cia.Rulebook:
        rule_file_body = """
        [module_a]
        operation = "not_allowed"
        imported_by = ["module_d"]
        """

        # TODO make importer_by to use blob or regex
        rules = cia.load_rulebook(
            rule_file_body,
        )
        return rules


    def test_allowed_to_import_by(self):
        python_mod_name = "module_d"
        python_mod_body = (
            "from module_a import func_a\n"
            "def hello_world():\n"
            "    print('Hello, World!')\n"
        )

        mod = cia.load_module(
            Path(python_mod_name),
            python_mod_body,
        )
        rulebook = self._build_rulebook()
        results = cia.apply_rulebook(mod, rulebook)
        self.assertTrue(len(results) == 1)
        self.assertTrue(results[0].status == cia.AppliedRuleStatus.FAILED)
