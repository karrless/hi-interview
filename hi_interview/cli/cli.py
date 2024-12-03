import fire  # type: ignore

from hi_interview.task_manager.task_manager import TaskManager


class TaskManagerCLI:
    """
    Клиент для управления задачами
    """

    def __init__(self) -> None:
        self.task_manager = TaskManager(
            tasks_file_name="tasks.json", options_file_name="options.json"
        )

    def add(
        self,
        title: str,
        description: str,
        category: str,
        due_date: str,
        priority: str | None = "3",
    ) -> str:
        """
        Добавить задачу

        Args:
            title (str): Имя задачи
            description (str): Описание задачи
            category (str): Категория задачи
            due_date (str): Дата выполнения
            priority (str | None): Приоритет задачи от 1 до 3, где 1 - высокий, 2 - средний, 3 - низкий. По умолчанию 3

        Returns:
            str: Сообщение о добавлении задачи
        """
        priority_value = int(priority) if priority else 1
        try:
            task = self.task_manager.add_task(
                title, description, category, due_date, priority_value
            )
        except ValueError as e:
            return str(e)
        return f"Задача добавлена: {task}"

    def list(
        self,
        keywords: str | None = None,
        categories: str | None = None,
        status: int | None = None,
    ) -> None:
        """
        Список задач

        Args:
            keywords (str | None, optional): Ключевые слова через запятую. По умолчанию None
            categories (str | None, optional): Категории через запятую. По умолчанию None
            status (int | None, optional): Статус 1 - выполнена, 0 - не выполнена. По умолчанию None
        
        Usage:
            python -m hi_interview list --keywords="keyword1,keyword2" --categories="category1,category2"
            python -m hi_interview list --status=1
            python -m hi_interview list keyword1,keyword2 category1,category2 1
            python -m hi_interview list
        """
        keywords_list = keywords.split(",") if keywords else None
        categories_list = categories.split(",") if categories else None
        status_bool = bool(status) if status is not None else None

        tasks = self.task_manager.get_tasks(keywords_list, categories_list, status_bool)
        if not tasks:
            print("Задач нет")
        for task in tasks:
            print(task)

    def delete(self, task_id: str | None = None, category: str | None = None) -> str:
        """
        Удалить задачу

        Args:
            task_id (str | None, optional): ID задачи. По умолчанию None.
            category (str | None, optional): Категория задач. По умолчанию 0.

        Returns:
            str: Сообщение о удалении задач
            
        """
        try:
            if task_id:
                self.task_manager.delete_task(task_id=int(task_id))
                return f"Задача с ID {task_id} удалена"
            elif category:
                self.task_manager.delete_task(category=category)
                return f"Задачи в категории {category} удалены"
            else:
                return "Укажите ID задачи или категорию для удаления"
        except ValueError as e:
            return str(e)

    def complete(self, task_id: str) -> str:
        """
        Отметить задачу как выполненную

        Args:
            task_id (str): ID задачи

        Returns:
            str: Сообщение о выполнении задачи
        """
        try:
            self.task_manager.complete_task(int(task_id))
        except ValueError as e:
            return str(e)
        return f"Задача с ID {task_id} отмечена как выполненная"

    def update(
        self,
        task_id: str,
        title: str | None = None,
        description: str | None = None,
        category: str | None = None,
        due_date: str | None = None,
        priority: str | None = None,
    ) -> str:
        """
        Обновить задачу

        Args:
            task_id (str): ID задачи
            title (str | None, optional): Новое название задачи. По умолчанию None.
            description (str | None, optional): Новое описание задачи. По умолчанию None.
            category (str | None, optional): Новая категория задачи. По умолчанию None.
            due_date (str | None, optional): Новая дата выполнения задачи. По умолчанию None.
            priority (str | None, optional): Новый приоритет задачи от 1 до 3, где 1 - высокий, 2 - средний, 3 - низкий. По умолчанию None

        Returns:
            str: Сообщение об обновлении задачи
        """
        kwargs = {}
        if title:
            kwargs["title"] = title
        if description:
            kwargs["description"] = description
        if category:
            kwargs["category"] = category
        if due_date:
            kwargs["due_date"] = due_date
        if priority:
            kwargs["priority"] = priority
        try:
            self.task_manager.update_task(int(task_id), **kwargs)
        except ValueError as e:
            return str(e)
        return f"Задача с ID {task_id} обновлена"


def run() -> None:
    fire.Fire(TaskManagerCLI)
