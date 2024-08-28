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
   
![Become_a_PRO_mindmap](https://github.com/kkhitalenko/Become_a_PRO/raw/main/mindmap.PNG)
   
</details>

<details>
   <summary>Как запустить?</summary> 
   Необходимые технологии: Docker, Docker-Compose

   <details>
   <summary>При первом запуске необходимо</summary> 
      
   1. Клонировать репозиторий и перейти в него в командной строке:
      ```
      git clone git@github.com:kkhitalenko/Become_a_PRO
      ```
      ```
      cd Become_a_PRO/infra/
      ```
   2. Создать .env файл и заполнить его по аналогии с файлом .env.example
   3. Запустить docker-compose:
      ```
      docker-compose up -d --build
      ```
   4. Последовательно выполнить следующие команды:
      ```
      docker-compose exec backend python manage.py migrate
      docker-compose exec backend python manage.py createsuperuser
      docker-compose exec backend python manage.py collectstatic --no-input 
      cat becomeapro.sql | docker exec -i BecomeaPRO_postgres psql -U postgres -d postgres
      ```
   </details>
   <details>
   <summary>При повторном запуске</summary> 
         
   1. Запустить docker-compose
      ```
      docker-compose up -d
      ```
   </details>
</details>

<details>
   <summary>Используемые инструменты и технологии</summary> 

- Python
- Poetry
- Pre-commit(Ruff)
- Django, DRF
- Gunicorn, Nginx
- Postgres
- Aiogram, Aiohttp
- Docker, Docker Compose
- Github Actions(CI:flake, isort)
<!-- Redis  --> 
<!-- Celery --> 
<!-- Pytest --> 

</details>
