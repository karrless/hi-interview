import pytest
from hi_interview.task_manager.task import Task, Priority, validate_and_format_date


@pytest.fixture
def sample_task() -> Task:
    """
    Create sample task

    Returns:
        Task: task
    """
    return Task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=Priority.LOW,
    )


def test_validate_and_format_date_valid() -> None:
    """
    Test validate and format date valid
    """
    assert validate_and_format_date("2003-12-28") == "28.12.2003"


def test_validate_and_format_date_invalid() -> None:
    """
    Test validate and format date invalid
    """
    with pytest.raises(ValueError):
        validate_and_format_date("2003-31-31")


def test_task_creation(sample_task: Task) -> None:
    """
    Test task creation

    Args:
        sample_task (Task): sample task
    """
    task = sample_task
    assert task.title == "Task 1"
    assert task.description == "Description 1"
    assert task.category == "Category 1"
    assert task.due_date == "28.12.2003"
    assert task.priority == Priority.LOW
    assert not task.status
    assert isinstance(task.id, int)


def test_complere_task(sample_task: Task) -> None:
    """
    Test complete task

    Args:
        sample_task (Task): sample task
    """
    task = sample_task
    task.complete()
    assert task.status


def test_to_dict(sample_task: Task) -> None:
    """
    Test task to dict

    Args:
        sample_task (Task): sample task
    """
    task = sample_task
    task_dict = task.to_dict()
    assert isinstance(task_dict, dict)
    assert task_dict["id"] == task.id
    assert task_dict["title"] == "Task 1"
    assert task_dict["description"] == "Description 1"
    assert task_dict["category"] == "Category 1"
    assert task_dict["due_date"] == "28.12.2003"
    assert task_dict["priority"] == 3
    assert not task_dict["status"]


def test_from_dict() -> None:
    """
    Test task from dict
    """
    task_data = {
        "id": 2,
        "title": "Task 2",
        "description": "Description 2",
        "category": "Category 2",
        "due_date": "2003-12-28",
        "priority": 2,
        "status": False,
    }

    task = Task.from_dict(task_data)
    assert isinstance(task, Task)
    assert task.id == 2
    assert task.title == "Task 2"
    assert task.description == "Description 2"
    assert task.category == "Category 2"
    assert task.due_date == "28.12.2003"
    assert task.priority == Priority.MEDIUM
    assert not task.status


def test_invalid_priority_in_dict() -> None:
    """
    Test invalid task from dict
    """
    task_data = {
        "id": 2,
        "title": "Task 2",
        "description": "Description 2",
        "category": "Category 2",
        "due_date": "2003-12-28",
        "priority": 4,
        "status": False,
    }

    with pytest.raises(ValueError):
        Task.from_dict(task_data)


def test_invalid_date_in_dict() -> None:
    """
    Test invalid task from dict
    """
    task_data = {
        "id": 2,
        "title": "Task 2",
        "description": "Description 2",
        "category": "Category 2",
        "due_date": "2003-31-31",
        "priority": 4,
        "status": False,
    }

    with pytest.raises(ValueError):
        Task.from_dict(task_data)


def test_invalid_from_dict() -> None:
    """
    Test invalid task from dict
    """
    task_data = {
        "title": "Task 1",
        "description": "Description 1",
        "category": "Category 1",
        "due_date": "2003-12-28",
        # "priority" отсутствует
        "status": False,
    }

    with pytest.raises(ValueError):
        Task.from_dict(task_data)
