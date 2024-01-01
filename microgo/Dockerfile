FROM python:3.10.12-slim
RUN pip install poetry==1.7.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./
COPY monolith ./monolith
COPY lib ./lib
RUN touch README.md

RUN poetry config virtualenvs.create false
RUN poetry install

WORKDIR /app/monolith

ENTRYPOINT ["poetry", "run", "gunicorn", "-c", "gunicorn_config.py", "server:app"]