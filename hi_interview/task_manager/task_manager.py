"""
Containts task manager class
"""

from typing import Any
from hi_interview.task_manager.task import Task, Priority
import json


class TaskManager:
    def __init__(
        self,
        tasks_file_name: str = "tasks.json",
        options_file_name: str = "options.json",
    ):
        """
        Task manager init

        Args:
            tasks_file_name (str, optional): File name with tasks. Defaults to "tasks.json".
            options_file_name (str, optional): File name with options. Defaults to "options.json".

        Raises:
            ValueError: File name with tasks must end with .json
            ValueError: File name with options must end with .json
        """

        if not tasks_file_name.endswith(".json"):
            raise ValueError("File name with tasks must end with .json")

        if not options_file_name.endswith(".json"):
            raise ValueError("File name with options must end with .json")

        self.tasks_file_name: str = tasks_file_name
        self.options_file_name: str = options_file_name
        self.tasks: list[Task] = self.load_tasks()
        self.options = self.load_options()

    def load_options(self) -> dict:
        """
        Load options from file
        Returns:
            dict: Options

        Raises:
            ValueError: Options file not found
        """
        try:
            with open(self.options_file_name, "r", encoding="utf-8") as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_options(self) -> None:
        """
        Save options to file
        """
        with open(self.options_file_name, "w", encoding="utf-8") as f:
            json.dump(self.options, f)

    def __get_next_id(self) -> int:
        """
        Get next id

        Returns:
            int: Next id

        Raises:
            ValueError: Last id not found
        """
        current_id = self.options.get("id")
        if not current_id:
            current_id = max((task.id for task in self.tasks), default=0) + 1
        self.options["id"] = current_id + 1
        self.save_options()
        return current_id

    def load_tasks(self) -> list[Task]:
        """
        Load tasks from file
        Returns:
            list[Task]: List of tasks
        """
        try:
            with open(self.tasks_file_name, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            return []

    def save_tasks(self) -> None:
        """
        Save tasks to file
        """
        with open(self.tasks_file_name, "w", encoding="utf-8") as f:
            json.dump([task.to_dict() for task in self.tasks], f)

    def add_task(
        self,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: int,
        status: bool = False,
    ) -> Task:
        """
        Add task

        Args:
            title (str): task title
            description (str): task description
            category (str): task category
            due_date (str): task due date
            priority (int): task priority
            status (bool, optional): task status. Defaults to False.

        Raises:
            ValueError: Invalid priority
            ValuerError: Invalid date
            ValueError: All arguments must be not empty

        Returns:
            Task: Created task
        """

        for arg in (title, description, category, due_date, priority):
            if not arg:
                raise ValueError("All arguments must be not empty")

        try:
            priority_enum = Priority(priority)
        except ValueError:
            raise ValueError("Invalid priority. Priority must be one of 1, 2 or 3")

        task = Task(
            id=self.__get_next_id(),
            title=title,
            description=description,
            category=category,
            due_date=due_date,
            priority=priority_enum,
            status=status,
        )

        self.tasks.append(task)
        self.save_tasks()

        return task

    def get_task(self, task_id: int) -> Task:
        """
        Get task by id

        Args:
            task_id (int): task id

        Raises:
            ValueError: Task not found

        Returns:
            Task: task
        """
        for task in self.tasks:
            if task.id == task_id:
                return task
        raise ValueError("Task not found")

    def delete_task(
        self, task_id: int | None = None, category: str | None = None
    ) -> None:
        """
        Delete task

        Args:
            task_id (int): task id
            category (str): task category

        Raises:
            ValueError: Task id or category must be provided
        """
        if task_id:
            self.tasks = [task for task in self.tasks if task.id != task_id]
        elif category:
            self.tasks = [task for task in self.tasks if task.category != category]
        else:
            raise ValueError("Task id or category must be provided")
        self.save_tasks()

    def update_task(self, task_id: int, **kwargs: Any) -> None:
        """
        Update task

        Args:
            task_id (int): task id
            kwargs: task fields

        Raises:
            ValueError: Task not found
        """
        for task in self.tasks:
            if task.id == task_id:
                task.update(**kwargs)
                self.save_tasks()
                break
        else:
            raise ValueError("Task not found")

    def complete_task(self, task_id: int) -> None:
        """
        Complete task

        Args:
            task_id (int): task id

        Raises:
            ValueError: Task not found
        """
        for task in self.tasks:
            if task.id == task_id:
                task.complete()
                self.save_tasks()
                break
        else:
            raise ValueError("Task not found")

    def get_tasks(
        self,
        keywords: list[str] | None = None,
        categories: list[str] | None = None,
        status: bool | None = None,
    ) -> list[Task]:
        """
        Get tasks by keywords, categories and status

        Args:
            keywords (list[str] | None, optional): keywords of tasks. Defaults to None.
            categories (list[str] | None, optional): categories of tasks. Defaults to None.
            status (bool | None, optional): status status of tasks. Defaults to None.

        Returns:
            list[Task]: List of tasks
        """
        return [
            task
            for task in self.tasks
            if (not keywords or any(keyword.lower() in task.title.lower().split() for keyword in keywords))
            and (
                not categories
                or any(category.lower() in task.category.lower() for category in categories)
            )
            and (not status or task.status == status)
        ]
