import pathlib
import pytest
from hi_interview.task_manager.task import Priority
from hi_interview.task_manager.task_manager import TaskManager


@pytest.fixture
def task_manager(tmp_path: pathlib.Path) -> TaskManager:
    """
    Create task manager

    Args:
        tmp_path (pathlib.Path): Temp path

    Returns:
        TaskManager: Task manager
    """
    tasks_file = tmp_path / "tasks.json"
    options_file = tmp_path / "options.json"
    return TaskManager(str(tasks_file), str(options_file))


def test_init_invalid_files() -> None:
    """
    Test init with invalid files
    """
    with pytest.raises(ValueError):
        TaskManager("invalid.txt", "options.json")
    with pytest.raises(ValueError):
        TaskManager("tasks.json", "invalid.txt")


def test_add_task(task_manager: TaskManager) -> None:
    """
    Test add task

    Args:
        task_manager (TaskManager): Task manager
    """
    task = task_manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=1,
    )
    assert task.title == "Task 1"
    assert task.description == "Description 1"
    assert task.category == "Category 1"
    assert task.due_date == "28.12.2003"
    assert task.priority == Priority.HIGH


def test_add_task_invalid_priority(task_manager: TaskManager) -> None:
    """
    Test add task with invalid priority

    Args:
        task_manager (TaskManager): Task manager
    """
    with pytest.raises(ValueError):
        task_manager.add_task(
            title="Task 1",
            description="Description 1",
            category="Category 1",
            due_date="2003-12-28",
            priority=4,  # Invalid priority
        )


def test_get_task(task_manager: TaskManager) -> None:
    """
    Test get task

    Args:
        task_manager (TaskManager): Task manager
    """
    task = task_manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=1,
    )
    fetched_task = task_manager.get_task(task.id)
    assert fetched_task == task


def test_get_task_not_found(task_manager: TaskManager) -> None:
    """
    Test get task not found

    Args:
        task_manager (TaskManager): Task manager
    """
    with pytest.raises(ValueError):
        task_manager.get_task(999)


def test_delete_task(task_manager: TaskManager) -> None:
    """
    Test delete task

    Args:
        task_manager (TaskManager): Task manager
    """
    task = task_manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=1,
    )
    task_manager.delete_task(task.id)
    assert len(task_manager.tasks) == 0


def test_update_task(task_manager: TaskManager) -> None:
    """
    Test update task

    Args:
        task_manager (TaskManager): Task manager
    """
    task = task_manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=1,
    )
    task_manager.update_task(task_id=task.id, title="Updated Task")
    updated_task = task_manager.get_task(task.id)
    assert updated_task.title == "Updated Task"


def test_update_task_not_found(task_manager: TaskManager) -> None:
    """
    Test update task not found

    Args:
        task_manager (TaskManager): Task manager
    """
    with pytest.raises(ValueError):
        task_manager.update_task(999, title="Updated Task")


def test_complete_task(task_manager: TaskManager) -> None:
    """
    Test complete task

    Args:
        task_manager (TaskManager): Task manager
    """
    task = task_manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=1,
    )
    task_manager.complete_task(task.id)
    assert task.status is True


def test_complete_task_not_found(task_manager: TaskManager) -> None:
    """
    Test complete task not found

    Args:
        task_manager (TaskManager): Task manager
    """
    with pytest.raises(ValueError):
        task_manager.complete_task(999)


def test_get_tasks_by_keywords(task_manager: TaskManager) -> None:
    """
    Test get tasks by keywords

    Args:
        task_manager (TaskManager): Task manager
    """
    task_manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Work",
        due_date="2003-12-28",
        priority=1,
    )
    task_manager.add_task(
        title="Important Task",
        description="Description 2",
        category="Home",
        due_date="2003-12-28",
        priority=2,
    )
    tasks = task_manager.get_tasks(keywords=["Important"])
    assert len(tasks) == 1
    assert tasks[0].title == "Important Task"


def test_get_tasks_by_category(task_manager: TaskManager) -> None:
    """
    Test get tasks by category

    Args:
        task_manager (TaskManager): Task manager
    """
    task_manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Work",
        due_date="2003-12-28",
        priority=1,
    )
    task_manager.add_task(
        title="Task 2",
        description="Description 2",
        category="Home",
        due_date="2003-12-28",
        priority=2,
    )
    tasks = task_manager.get_tasks(categories=["Work"])
    assert len(tasks) == 1
    assert tasks[0].category == "Work"


def test_save_and_load_tasks(task_manager: TaskManager) -> None:
    """
    Test save and load tasks

    Args:
        task_manager (TaskManager): Task manager
    """
    task_manager.add_task(
        title="Persistent Task",
        description="Description",
        category="Work",
        due_date="2003-12-28",
        priority=1,
    )
    task_manager.save_tasks()

    # Reload from saved file
    new_task_manager = TaskManager(
        task_manager.tasks_file_name, task_manager.options_file_name
    )
    assert len(new_task_manager.tasks) == 1
    assert new_task_manager.tasks[0].title == "Persistent Task"
