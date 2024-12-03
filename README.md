# Task Manager CLI for Hitalent
## Описание
Этот репозиторий содержит тестовое задание на собеседование в компанию Hitalent: cli программу для работы с задачами

## Установка
1. Клонировать репозиторий
   ```    
   git clone https://github.com/karrless/hi-interview.git
   ```
2. Перейти в созданный репозиторий
   ```
   cd hi-interview
   ```
3. Установить вcе зависимости
   1. С Poetry:
        ```
        poetry install
        ```
   2. Без Poetry:
        ```
        pip install -r requirements.txt

        ```

## Использование
Дальнейшая работа с cli произодится следующим образом:

С Poetry:
```
poetry run tasks
```
Без poetry:
```
python -m hi-interview
```

Для просмотра команд необхоидмо просто запустить скрипт:
```
poetry run tasks
```
Для просмотра помощи по той или иной команде необходимо ввести:
```
poetry run tasks <command> --help
```
или 
```
poetry run tasks <command> -h
```