### Для запуска необходимо:

- Перейти в папку в которой будем работать
-
    - path_to_dir ваша рабочая директория
- `cd path_to_dir`
- Склонировать репозиторий
- `git clone https://github.com/Nudlik/django_first_project.git`
- Cоздать виртуальное окружение
- `python -m venv venv`
- Активировать виртуальное окружение
- `.\venv\Scripts\activate`
- Установить зависимости
- `pip install -r requirements.txt`
- Прописать в .env ваши настройки(пример файла .env.example):
- Приминить миграции
- `python .\manage.py migrate`
- Запустить файл, который заполнит таблицы данными из фикстуры
- `python .\manage.py load_my_data`
- Запустить программу/запустить программу из среды разработки
- `python .\manage.py runserver`