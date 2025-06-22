import unittest
from pathlib import Path

import cia


class ImportingRulesTestCase(unittest.TestCase):

    def test_parse_empty_rule_file(self):
        rule_file_body = ""
        rules = cia.load_rules(
            rule_file_body,
        )
        self.assertTrue(isinstance(rules, dict))
        self.assertTrue(len(rules) == 0)

    def test_parse_importees_only_file(self):
        rule_file_body = """
        [importees.module_c]
        allowed = ["module_d"]
        """
        rules = cia.load_rules(
            rule_file_body,
        )
        self.assertTrue(isinstance(rules, dict))
        self.assertTrue(rules.get("importees"))
        self.assertTrue(rules["importees"].get("module_c"))
        self.assertTrue(rules["importees"]["module_c"].get("allowed"))
        self.assertTrue(len(rules["importees"]["module_c"]["allowed"]) == 1)

    def test_parse_importers_only_file(self):
        rule_file_body = """
        [importers.module_d]
        allowed = ["module_c"]
        """
        rules = cia.load_rules(
            rule_file_body,
        )
        self.assertTrue(isinstance(rules, dict))
        self.assertTrue(rules.get("importers"))
        self.assertTrue(rules["importers"].get("module_d"))
        self.assertTrue(rules["importers"]["module_d"].get("allowed"))
        self.assertTrue(len(rules["importers"]["module_d"]["allowed"]) == 1)


class ImporteesTestCase(unittest.TestCase):

    def test_

