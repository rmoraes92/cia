import unittest
# from pathlib import Path

import cia


class ParsingRulebookTestCase(unittest.TestCase):

    def test_parsing_with_dataclasses(self):
        rule_file_body = """
        [[rules]]
        module = "path.to.module_a.*"
        modality = "allowed"
        imported_by = [
            "path.to.module_b",
            "path.to.module_c",
            "path.to.module_d"
        ]

        [[rules]]
        module = "path.to.module_a.*"
        modality = "allowed"
        imported_by = [
            "path.to.module_b",
            "path.to.module_c",
            "path.to.module_d"
        ]
        """

        rules = cia.load_rulebook(
            rule_file_body,
        )
        self.assertTrue(isinstance(rules, cia.Rulebook))
        self.assertTrue(len(rules.rules) == 1)
