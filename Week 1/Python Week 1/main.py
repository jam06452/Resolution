import argparse
import sys
import os
import json

TASK_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []

def save_task(tasks):
    with open(TASK_FILE, "w") as file:
        json.dump(tasks, file, indent=2)

parser = argparse.ArgumentParser()
parser.add_argument("task", type=str, nargs="?", help="Task to add")
parser.add_argument("-c", "--complete", type=int, help="Mark a task complete by ID")
parser.add_argument("-d", "--delete", type=int, help="Delete a task by ID")
parser.add_argument("-l", "--list", help="List all tasks", action="store_true")
args = parser.parse_args()

if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if args.task:
    tasks = load_tasks()
    if len(tasks) == 0:
        new_id = 1
    else: 
        new_id = tasks[-1]["id"] + 1
    tasks.append({"id": new_id, "task": args.task, "done": False})
    save_task(tasks)

    print(f"Task {args.task} added with an ID of {new_id}")

elif args.complete:
    tasks = load_tasks()
    for task in tasks:
        if task["id"] == args.complete:
            task["done"] = True
            save_task(tasks)
            print(f"Task {args.complete} marked as complete")
            break

elif args.delete:
    tasks = load_tasks()
    new_task = []
    for task in tasks:
        if task["id"] != args.delete:
            new_task.append(task)
