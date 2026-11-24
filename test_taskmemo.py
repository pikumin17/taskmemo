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

    def run_raw(self, *args):
        return subprocess.run(
            [sys.executable, "-X", "utf8", str(SCRIPT), *args],
            cwd=self.workdir,
            capture_output=True,
            encoding="utf-8",
        )

    def run_taskmemo(self, *args):
        result = self.run_raw(*args)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout

    def load_saved(self):
        return json.loads((self.workdir / "tasks.json").read_text(encoding="utf-8"))

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

    def test_done_marks_only_the_specified_task_in_list(self):
        self.run_taskmemo("add", "買い物に行く")
        self.run_taskmemo("add", "メールを返信する")

        self.assertEqual(self.run_taskmemo("done", "2"), "")
        self.assertEqual(
            self.run_taskmemo("list").splitlines(),
            ["1: 買い物に行く", "2: [完了] メールを返信する"],
        )

    def test_done_persists_completion_without_touching_other_tasks(self):
        self.run_taskmemo("add", "買い物に行く")
        self.run_taskmemo("add", "メールを返信する")

        self.run_taskmemo("done", "1")

        self.assertEqual(
            self.load_saved(),
            [
                {"id": 1, "text": "買い物に行く", "done": True},
                {"id": 2, "text": "メールを返信する"},
            ],
        )

    def test_done_looks_up_tasks_by_id_not_position(self):
        tasks = [{"id": 3, "text": "掃除する"}, {"id": 7, "text": "本を読む"}]
        (self.workdir / "tasks.json").write_text(
            json.dumps(tasks, ensure_ascii=False), encoding="utf-8"
        )

        self.run_taskmemo("done", "7")

        self.assertEqual(
            self.load_saved(),
            [
                {"id": 3, "text": "掃除する"},
                {"id": 7, "text": "本を読む", "done": True},
            ],
        )

    def test_done_with_unknown_id_fails_without_changing_tasks(self):
        self.run_taskmemo("add", "買い物に行く")
        task_file = self.workdir / "tasks.json"
        before = task_file.read_bytes()

        for task_id in ("0", "-1", "99"):
            with self.subTest(task_id=task_id):
                result = self.run_raw("done", task_id)

                self.assertNotEqual(result.returncode, 0)
                self.assertIn(f"error: task {task_id} not found", result.stderr)
                self.assertNotIn("Traceback", result.stdout + result.stderr)
                self.assertEqual(task_file.read_bytes(), before)

    def test_done_with_missing_save_file_fails_without_creating_it(self):
        result = self.run_raw("done", "1")

        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.workdir / "tasks.json").exists())
