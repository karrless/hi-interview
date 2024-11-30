"""
Containts task class
"""

from enum import Enum
from dateutil import parser # type: ignore
from typing import Self
import uuid


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
        title (str): task title
        description (str): task description
        category (str): task category
        due_date (str): task due date
        priority (Priority): task priority
        status (bool): task status
    """

    def __init__(
        self,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: Priority,
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

        self.id: int = uuid.uuid4().int
        self.title: str = title
        self.description: str = description
        self.category: str = category
        self.due_date: str = validate_and_format_date(due_date)
        self.priority: Priority = priority
        self.status: bool = status

    def complete(self)-> None:
        """
        Complete task
        """
        self.status = True

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
