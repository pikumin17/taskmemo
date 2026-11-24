import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().with_name("taskmemo.py")


class TaskMemoTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.workdir = Path(folder.name)

    def run_taskmemo(self, *args):
        result = subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), *args],
            cwd=self.workdir,
            capture_output=True,
            encoding="utf-8",
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def test_add_persists_tasks_with_sequential_ids(self):
        self.run_taskmemo("add", "買い物に行く")
        self.run_taskmemo("add", "メールを返信する")

        saved = json.loads((self.workdir / "tasks.json").read_text(encoding="utf-8"))
        self.assertEqual(
            saved,
            [
                {"id": 1, "text": "買い物に行く"},
                {"id": 2, "text": "メールを返信する"},
            ],
        )

    def test_list_displays_saved_ids_and_descriptions(self):
        self.run_taskmemo("add", "買い物に行く")
        self.run_taskmemo("add", "メールを返信する")

        self.assertEqual(
            self.run_taskmemo("list").splitlines(),
            ["1: 買い物に行く", "2: メールを返信する"],
        )

    def test_list_is_empty_when_the_save_file_is_missing(self):
        self.assertEqual(self.run_taskmemo("list"), "")
        self.assertFalse((self.workdir / "tasks.json").exists())
