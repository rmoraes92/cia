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

        [module_d]
        operation = "allowed"
        import_from = ["module_a"]
        """
        rules = cia.load_rulebook(
            rule_file_body,
        )
        self.assertTrue(isinstance(rules, cia.Rulebook))
        self.assertTrue(len(rules.rules) == 2)


class ParsingPythonModuleTestCase(unittest.TestCase):

    def test_parsing_import_statements(self):
        python_mod_body = (
            "import a\n" "def hello_world():\n" "    print('Hello, World!')\n"
        )

        imports = cia.parse_import_statements(python_mod_body)

        self.assertTrue(len(imports) == 1)
        self.assertTrue(imports[0].root == "a")

        python_mod_body = (
            "from a import func_a\n"
            "def hello_world():\n"
            "    print('Hello, World!')\n"
        )

        imports = cia.parse_import_statements(python_mod_body)

        self.assertTrue(len(imports) == 1)
        self.assertTrue(imports[0].root == "a")
        self.assertTrue(len(imports[0].children) == 1)
        self.assertTrue(imports[0].children[0] == "func_a")
