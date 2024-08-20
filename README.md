![Become_a_PRO_workflow](https://github.com/kkhitalenko/Become_a_PRO/actions/workflows/CI.yml/badge.svg)

# become a PRO - Telegram бот для изучения языков программирования
С помощью данного бота можно изучать языки программирования, на данный момент доступны: Python, Go и Rust.

<details>
   <summary>Реализованные команды</summary> 

- /help - помощь
- /start - начать обучение
- /continue - продолжить обучение
- /repeat - повторить сложные вопросы 
- /switch_language - переключиться на другой язык
- /feedback - предложить автору идею или сообщить об ошибке
- /github - посмотреть код Become_a_PRO на github и поставить ⭐️

</details>

<details>
   <summary>Логика бота</summary> 
   
![Image alt](https://github.com/kkhitalenko/Become_a_PRO/raw/main/mindmap.PNG)
   
</details>

<details>
   <summary>Для запуска необходимо</summary> 

Необходимые технологии: Docker, Docker-Compose

- Клонировать репозиторий и перейти в него в командной строке:
   ```
   git clone git@github.com:kkhitalenko/Become_a_PRO
   ```
   ```
   cd Become_a_PRO/infra/
   ```
- Создать .env файл и заполнить его по аналогии с файлом .env.example
- Запустить docker-compose:
   ```
   docker-compose up -d --build
   ```
- Последовательно выполнить следующие команды:
   ```
   docker-compose exec backend python manage.py migrate
   docker-compose exec backend python manage.py createsuperuser
   docker-compose exec backend python manage.py collectstatic --no-input 
   ```

- Выполнить следующую команду с указанием ваших db-user и db-name
   ```
   cat becomeapro.sql | docker exec -i BecomeaPRO_postgres psql -U <db-user> -d <db-name>
   ```
</details>

<details>
   <summary>Используемые инструменты и технологии</summary> 
   
- Poetry
- Pre-commit(ruff)
- Python
- Django
- DRF
- Aiogram
- Aiohttp
- Postgres
- Docker, Docker Compose
- Github Actions(CI:flake, isort)
<!-- Celery --> 
<!-- Redis --> 
<!-- Pytest --> 
<!-- K8s --> 

</details>
