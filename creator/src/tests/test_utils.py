import os
from pathlib import Path
import yaml
import unittest
from ..worldbuilder.utils import local_yaml_writer, load_prompt, PROMPT_DIR


class TestLocalYamlWriter(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path("/tmp/world_builder_tests")
        self.tmp_dir.mkdir(parents=True, exist_ok=True)
        self.file = self.tmp_dir / "test.yaml"

    def tearDown(self):
        if self.file.exists():
            self.file.unlink()

    def test_write_dict(self):
        data = {"a": 1, "b": 2}
        msg = local_yaml_writer(str(self.file), data)
        self.assertTrue(self.file.exists())
        written = yaml.safe_load(self.file.read_text())
        self.assertEqual(written, data)
        self.assertIn("Successfully wrote", msg)

    def test_write_string(self):
        content = "foo: bar"
        msg = local_yaml_writer(str(self.file), content)
        self.assertTrue(self.file.exists())
        self.assertEqual(self.file.read_text(), content)
        self.assertIn("Successfully wrote", msg)

    def test_invalid_extension(self):
        msg = local_yaml_writer("bad.txt", "a: 1")
        self.assertEqual(msg, "Error: Filename must end with .yaml")


class TestLoadPrompt(unittest.TestCase):
    def test_load_prompt_reads_file(self):
        prompt_file = PROMPT_DIR / "create_world.txt"
        content = load_prompt("create_world.txt")
        self.assertTrue(len(content) > 0)
        self.assertEqual(content, prompt_file.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
