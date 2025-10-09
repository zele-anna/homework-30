FROM python:3.13

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction \
    && rm -rf /root/.cache/pypoetry

COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ["sh", "-c", "python manage.py collectstatic --noinput && gunicorn config.wsgi:application --bind 0.0.0.0:8000"]
