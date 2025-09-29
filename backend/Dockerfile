FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry==2.1

COPY pyproject.toml poetry.lock* ./
#COPY requirements.txt .

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction
#RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD poetry run alembic upgrade head && \
    poetry run uvicorn --host=0.0.0.0 app.main:app