"""
Containts task class
"""

from enum import Enum
from dateutil import parser  # type: ignore
from typing import Self


class Priority(Enum):
    """
    Enum of task priorities

    Args:
        LOW (int): Low priority
        MEDIUM (int): Medium priority
        HIGH (int): High priority
    """

    LOW = 3
    MEDIUM = 2
    HIGH = 1


def validate_and_format_date(date_str: str) -> str:
    """
    Validate and format date

    Args:
        date_str (str): date

    Raises:
        ValueError: Invalid date

    Returns:
        str: DD.MM.YYYY
    """
    try:
        date_obj = parser.parse(date_str)
        return date_obj.strftime("%d.%m.%Y")
    except (ValueError, TypeError):
        raise ValueError("Invalid date")


class Task:
    """
    Task

    Attributes:
        id (int): task id
        title (str): task title
        description (str): task description
        category (str): task category
        due_date (str): task due date
        priority (Priority): task priority. Defaults to Priority.LOW
        status (bool): task status. Defaults to False.
    """

    def __init__(
        self,
        id: int,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: Priority = Priority.LOW,
        status: bool = False,
    ):
        """
        Task init

        Args:
            title (str): task title
            description (str): task description
            category (str): task category
            due_date (str): task due date
            priority (Priority): task priority
            status (bool, optional): task status. Defaults to False.

        Raises:
            ValueError: Invalid date
        """

        self.id: int = id
        self.title: str = title
        self.description: str = description
        self.category: str = category
        self.due_date: str = validate_and_format_date(due_date)
        self.priority: Priority = priority
        self.status: bool = status

    def complete(self) -> None:
        """
        Complete task
        """
        self.status = True

    def update(
        self,
        title: str | None = None,
        description: str | None = None,
        category: str | None = None,
        due_date: str | None = None,
        priority: Priority | None = None,
    ) -> None:
        """
        Update task

        Args:
            title (str | None): new title
            description (str | None): new description
            category (str | None): new category
            due_date (str | None): new due date
            priority (Priority | None): new priority

        Raises:
            ValueError: Invalid date
        """
        self.title = title if title else self.title
        self.description = description if description else self.description
        self.category = category if category else self.category
        self.due_date = (
            validate_and_format_date(due_date) if due_date else self.due_date
        )
        self.priority = priority if priority else self.priority

    def to_dict(self) -> dict:
        """
        Convert task to dict

        Returns:
            dict: task data

        Example:
            >>> task = Task(1, "Task 1", "Description 1", "Category 1", "2021-01-01", Priority.LOW)
            >>> task_data = task.to_dict()
            >>> print(task_data)
            {'id': 1, 'title': 'Task 1', 'description': 'Description 1', 'category': 'Category 1', 'due_date': '2021-01-01', 'priority': 'LOW', 'status': false}
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority.value,
            "status": self.status,
        }

    def __repr__(self) -> str:
        text = (
            f'{self.id}. {self.title} --> {self.due_date}\n'
            f'\t{self.description}\n'
            f'\t{self.category} ({self.priority.name})\n'
            f'\t{"Выполнено" if self.status else "Не выполнено"}\n'
        )
        return text

    @classmethod
    def from_dict(cls: type[Self], task_data: dict) -> Self:
        """
        Create task from dict

        Args:
            task_data (dict): task data

        Raises:
            ValueError: Invalid task data

        Returns:
            Task: task

        Example:
            >>> task_data = {
                "id": 1,
                "title": "Task 1",
                "description": "Description 1",
                "category": "Category 1",
                "due_date": "2021-01-01",
                "priority": 3,
                "status": false
            }
            >>> task = Task.from_dict(task_data)
            >>> print(task.id)
            1
        """
        try:
            task = cls(
                id=task_data["id"],
                title=task_data["title"],
                description=task_data["description"],
                category=task_data["category"],
                due_date=task_data["due_date"],
                priority=Priority(task_data["priority"]),
                status=task_data["status"],
            )
            task.id = task_data["id"]
            return task
        except KeyError:
            raise ValueError("Invalid task data")
