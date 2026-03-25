### Hexlet tests and linter status:
[![Actions Status](https://github.com/OlegRakhilov/python-project-52/actions/workflows/hexlet-check.yml/badge.svg)](https://github.com/OlegRakhilov/python-project-52/actions)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=OlegRakhilov_python-project-52&metric=coverage)](https://sonarcloud.io/summary/new_code?id=OlegRakhilov_python-project-52)


### [Посмотреть демо на Render](https://python-project-52-phta.onrender.com)
## 📌 Описание
Учебный backend/CLI проект на Python, реализующий работу с данными и пользовательскими командами.

Приложение позволяет обрабатывать данные, выполнять команды и работать с файлами.

## ⚙️ Стек
- Python
- PostgreSQL (если есть)
- Git
- Linux
- Docker (если использовал)

## 🚀 Функциональность
- Обработка пользовательских команд
- Работа с данными (CRUD / чтение / запись)
- Логика приложения и структурирование кода
- Работа с файлами / конфигурациями

# Django Task Manager
Менеджер задач — это система управления проектами, написанная на Python и Django. Она позволяет ставить задачи, назначать исполнителей, менять статусы и фильтровать список дел.


## Установка и запуск

### Требования
* Python 3.10+
* Менеджер пакетов [uv](https://github.com)

### Шаги
1. Склонируйте репозиторий:
   ```bash
   git clone https://github.com
   cd python-project-52

2. Установите зависимости:
    uv sync

3. Выполните миграции:
    uv run python manage.py migrate

4. Запустите сервер:
    uv run python manage.py runserver

5. Тестирование
    uv run python manage.py test