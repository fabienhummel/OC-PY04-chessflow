"""Architecture checks for independent business models."""

import ast
import unittest
from pathlib import Path


class ModelIndependenceTestCase(unittest.TestCase):
    """Ensure models never depend on views or controllers."""

    def test_each_model_module_imports_independently(self) -> None:
        from models.match import Match
        from models.player import Player
        from models.round import Round
        from models.tournament import Tournament

        self.assertEqual({Match.__name__, Player.__name__, Round.__name__, Tournament.__name__}, {
            "Match", "Player", "Round", "Tournament"
        })

    def test_models_do_not_import_views_or_controllers(self) -> None:
        model_directory = Path(__file__).parents[1] / "models"
        forbidden_roots = {"views", "controllers"}

        for model_path in model_directory.glob("*.py"):
            with self.subTest(model=model_path.name):
                tree = ast.parse(model_path.read_text(encoding="utf-8"))
                imported_roots = {
                    alias.name.split(".")[0]
                    for node in ast.walk(tree)
                    if isinstance(node, ast.Import)
                    for alias in node.names
                }
                imported_roots.update(
                    node.module.split(".")[0]
                    for node in ast.walk(tree)
                    if isinstance(node, ast.ImportFrom) and node.module
                )
                self.assertFalse(imported_roots & forbidden_roots)


if __name__ == "__main__":
    unittest.main()
