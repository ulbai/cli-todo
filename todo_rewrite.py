import sys
import json
from pathlib import Path

# 增
# 查
# 改
# 删
# 加载
# 保存
# 解析id

file_path = Path("tasks.json")


def load_tasks():
    if file_path.exists():
        return json.loads(file_path.read_text(encoding="utf-8"))
    return []


def save_tasks(tasks):
    file_path.write_text(json.dumps(tasks, ensure_ascii=False, indent=2))


def add_task(title):
    tasks = load_tasks()

    if tasks:
        task_id = max(task["id"] for task in tasks) + 1
    else:
        task_id = 1

    task = {"id": task_id, "title": title, "done": False}

    tasks.append(task)
    save_tasks(tasks)

    print("任务已添加")


def list_tasks():
    tasks = load_tasks()

    for task in tasks:
        status = "[x]" if task["done"] else "[ ]"
        print(f"{task['id']}. {status} {task['title']}")


def find_task(tasks, task_id):
    for task in tasks:
        if task_id == task["id"]:
            return task
    return None


def parse_task_id():
    if len(sys.argv) != 3:
        raise ValueError("缺少任务ID")

    try:
        return int(sys.argv[2])
    except ValueError:
        raise ValueError("任务ID必须是数字")


def complete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task:
        task["done"] = True
        save_tasks(tasks)
        print("任务已完成")
    else:
        print("任务不存在")


def delete_task(task_id):
    tasks = load_tasks()
    task = find_task(tasks, task_id)

    if task:
        tasks.remove(task)
        save_tasks(tasks)
        print("任务已删除")
    else:
        print("任务不存在")


def main():
    if len(sys.argv) < 2:
        print("用法: python todo_rewrite.py <命令>")
        return

    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) != 3:
            print("用法: python todo_rewrite.py add <任务>")
            return
        add_task(sys.argv[2])

    elif command == "list":
        if len(sys.argv) != 2:
            print("用法: python todo_rewrite.py list")
            return
        list_tasks()

    elif command == "done":
        try:
            task_id = parse_task_id()
        except ValueError as e:
            print(e)
            return

        complete_task(task_id)

    elif command == "delete":
        task_id = parse_task_id()
        delete_task(task_id)

    else:
        print(f"未知命令:{command}")


if __name__ == "__main__":
    main()
