FROM python:3.11-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false
RUN poetry install

COPY ./ .

CMD ["gunicorn", "Become_a_PRO.wsgi:application", "--bind", "0:8000"]
