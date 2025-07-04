import unittest
from pathlib import Path

import cia


class ApplyRulesTestCase(unittest.TestCase):

    def test_apply_allowed_to_import(self):
        rule_file_body = """
        [[rules]]
        module = "path.to.module_a.*"
        modality = "allowed"
        imported_by = [
            "path.to.module_b"
        ]
        """

        rules = cia.load_rulebook(
            rule_file_body,
        )
        module = cia.load_module(
            Path("path.to.module_b"),
            "from path.to.module_a import func_a"
        )
        results = cia.apply_rulebook(
            module,
            rules,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, cia.AppliedRuleStatus.PASSED)

    def test_apply_not_allowed_to_import(self):
        rule_file_body = """
        [[rules]]
        module = "path.to.module_a.*"
        modality = "not_allowed"
        imported_by = [
            "path.to.module_b"
        ]
        """

        rules = cia.load_rulebook(
            rule_file_body,
        )
        module = cia.load_module(
            Path("path.to.module_b"),
            "from path.to.module_a import func_a"
        )
        results = cia.apply_rulebook(
            module,
            rules,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].status, cia.AppliedRuleStatus.FAILED)
