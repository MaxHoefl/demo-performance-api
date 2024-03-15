# Use the official Python Alpine image as base
FROM python:3.10.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

## Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    unixodbc-dev \
    gcc \
    g++

# Install Poetry
RUN pip install poetry==1.6.1

# Copy the poetry files and install dependencies
WORKDIR /src
COPY ./pyproject.toml ./poetry.lock /src/
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi --without dev

# Copy the FastAPI server script
COPY ./app /src/app

# Expose port 8000
EXPOSE 8080

# Command to run the FastAPI server
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
