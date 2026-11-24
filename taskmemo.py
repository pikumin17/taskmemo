import argparse
import json
import sys
from pathlib import Path


def save_tasks(task_file, tasks):
    task_file.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def main():
    parser = argparse.ArgumentParser(description="Manage a local task list.")
    commands = parser.add_subparsers(dest="command", required=True)

    add = commands.add_parser("add", help="Add a task")
    add.add_argument("text", help="Task description")
    commands.add_parser("list", help="List tasks")
    done = commands.add_parser("done", help="Mark a task as done")
    done.add_argument("id", type=int, help="Task ID shown by list")

    args = parser.parse_args()
    task_file = Path("tasks.json")
    try:
        tasks = json.loads(task_file.read_text(encoding="utf-8"))
    except FileNotFoundError:
        tasks = []

    if args.command == "add":
        next_id = max((task["id"] for task in tasks), default=0) + 1
        tasks.append({"id": next_id, "text": args.text})
        save_tasks(task_file, tasks)
    elif args.command == "list":
        for task in tasks:
            mark = "[完了] " if task.get("done", False) else ""
            print(f"{task['id']}: {mark}{task['text']}")
    elif args.command == "done":
        for task in tasks:
            if task["id"] == args.id:
                task["done"] = True
                save_tasks(task_file, tasks)
                break
        else:
            print(f"error: task {args.id} not found", file=sys.stderr)
            sys.exit(1)


if __name__ == "__main__":
    main()
