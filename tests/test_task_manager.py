import pytest
from py._path.local import LocalPath # type: ignore
from hi_interview.task_manager import Task, Priority, TaskManager



@pytest.fixture
def task_manager(tmpdir: LocalPath) -> tuple[TaskManager, str]:
    """
    Fixture for creating a task manager

    Args:
        tmpdir (LocalPath): Temporary directory

    Returns:
        tuple[TaskManager, str]: Task manager and file name
    """
    file_name = tmpdir.join("tasks.json")
    manager = TaskManager(file_name=str(file_name))
    return manager, str(file_name)


def test_add_task(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing adding a task

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    task: Task = manager.add_task(
        title="Test Task",
        description="Test Description",
        category="Test Category",
        due_date="2003-12-28",
        priority=2,
    )

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.category == "Test Category"
    assert task.due_date == "28.12.2003"
    assert task.priority == Priority.MEDIUM
    assert not task.status 
    assert isinstance(task.id, int)


def test_add_task_invalid_priority(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing adding a task with invalid priority

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    with pytest.raises(ValueError, match="Invalid priority. Priority must be one of 1, 2 or 3"):
        manager.add_task(
            title="Test Task",
            description="Test Description",
            category="Test Category",
            due_date="2003-12-28",
            priority=999,
        )


def test_add_task_empty_field(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing adding a task with empty field

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    with pytest.raises(ValueError, match="All arguments must be not empty"):
        manager.add_task(
            title="",
            description="Test Description",
            category="Test Category",
            due_date="2003-12-28",
            priority=3,
        )



def test_get_task(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing getting a task

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    task: Task = manager.add_task(
        title="Test Task",
        description="Test Description",
        category="Test Category",
        due_date="2003-12-28",
        priority=2,
    )

    task_id: int = task.id
    retrieved_task: Task = manager.get_task(task_id)

    assert task.id == retrieved_task.id
    

def test_get_task_not_found(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing getting a task that doesn't exist

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    with pytest.raises(ValueError, match="Task not found"):
        manager.get_task(999999)


def test_delete_task(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing deleting a task

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    task: Task = manager.add_task(
        title="Test Task",
        description="Test Description",
        category="Test Category",
        due_date="2003-12-28",
        priority=2,
    )

    task_id: int = task.id
    manager.delete_task(task_id)

    tasks: list[Task] = manager.get_tasks()
    assert not any(t.id == task_id for t in tasks)


def test_complete_task(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing completing a task

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    task: Task = manager.add_task(
        title="Test Task",
        description="Test Description",
        category="Test Category",
        due_date="2003-12-28",
        priority=2,
    )

    task_id: int = task.id
    manager.complete_task(task_id)

    completed_task: Task = manager.get_task(task_id)
    assert completed_task.status

def test_complete_task_not_found(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing completing a task that doesn't exist

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    with pytest.raises(ValueError, match="Task not found"):
        manager.complete_task(999999)  # Не существует задачи с таким ID


def test_get_tasks(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing getting tasks

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, _ = task_manager
    manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=3,
    )
    manager.add_task(
        title="Task 2",
        description="Description 2",
        category="Category 2",
        due_date="2003-12-28",
        priority=1,
    )

    tasks_by_category: list[Task] = manager.get_tasks(categories=["Category 1"])
    tasks_by_keywords: list[Task] = manager.get_tasks(keywords=["Task 1"])
    tasks_by_status: list[Task] = manager.get_tasks(status=False)

    assert len(tasks_by_category) == 1
    assert len(tasks_by_keywords) == 1
    assert len(tasks_by_status) == 2


def test_load_tasks_from_file(task_manager: tuple[TaskManager, str]) -> None:
    """
    Testing loading tasks from file

    Args:
        task_manager (tuple[TaskManager, str]): Task manager and file name
    """
    manager, file_name = task_manager
    manager.add_task(
        title="Task 1",
        description="Description 1",
        category="Category 1",
        due_date="2003-12-28",
        priority=3,
    )
    manager.add_task(
        title="Task 2",
        description="Description 2",
        category="Category 2",
        due_date="2003-12-28",
        priority=1,
    )
    
    # Сохраняем задачи в файл
    manager.save_tasks()

    # Создаем новый менеджер с тем же файлом и проверяем, что задачи загрузились
    new_manager: TaskManager = TaskManager(file_name=str(file_name))
    tasks: list[Task] = new_manager.get_tasks()

    assert len(tasks) == 2
    assert tasks[0].title == "Task 1"
    assert tasks[1].title == "Task 2"
