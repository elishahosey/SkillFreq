FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
    JOBSPY_DATA_PATH=/app/Jobspy

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libffi-dev \
        libxml2-dev \
        libxslt1-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt \
    && python -m playwright install --with-deps chromium

COPY configs ./configs
COPY skillfreq ./skillfreq
COPY Jobspy ./Jobspy
COPY README.md .

RUN mkdir -p data/inputs data/outputs logging

ENTRYPOINT ["python", "-m", "skillfreq.cli"]
CMD ["--help"]
