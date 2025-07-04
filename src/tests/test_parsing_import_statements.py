import unittest
import cia


class ParsingImportStatementsTestCase(unittest.TestCase):

    def test_parse_import_statements(self):
        import_statements = cia.parse_import_statements(
            "import sys\n"
            "from math import sqrt\n"
            "import pathlib.Path\n"
            "from foo.bar import baz\n"
            "from doo.boo import (zee, wee)\n"
            "from .goo.loo import (zee, wee)\n"
        )
        self.assertEqual(import_statements[0].absolute_paths()[0], "sys")
        self.assertEqual(import_statements[1].absolute_paths()[0], "math.sqrt")
        self.assertEqual(
            import_statements[2].absolute_paths()[0], "pathlib.Path")
        self.assertEqual(
            import_statements[3].absolute_paths()[0], "foo.bar.baz")
        self.assertEqual(
            import_statements[4].absolute_paths()[0], "doo.boo.zee")
        self.assertEqual(
            import_statements[4].absolute_paths()[1], "doo.boo.wee")
        self.assertEqual(
            import_statements[5].absolute_paths()[0], "goo.loo.zee")
        self.assertEqual(
            import_statements[5].absolute_paths()[1], "goo.loo.wee")
