import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="Manage a local task list.")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add a task")
    add.add_argument("text", help="Task description")
    commands.add_parser("list", help="List tasks")

    args = parser.parse_args()
    task_file = Path("tasks.json")
    try:
        tasks = json.loads(task_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        tasks = []

    if args.command == "add":
        next_id = max((task["id"] for task in tasks), default=0) + 1
        tasks.append({"id": next_id, "text": args.text})
        task_file.write_text(
            json.dumps(tasks, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    else:
        for task in tasks:
            print(f"{task['id']}: {task['text']}")


if __name__ == "__main__":
    main()
