FROM python:3.10.9-bullseye as base

WORKDIR /app

COPY requirements.txt ./
RUN PIP_ROOT_USER_ACTION=ignore pip install --upgrade pip && \
    PIP_ROOT_USER_ACTION=ignore pip install  -r requirements.txt

COPY /tilly ./tilly

ARG GIT_METADATA=dockerfile
ENV GIT_METADATA=$GIT_METADATA
ENV PYTHONPATH app

EXPOSE 8000
CMD ["gunicorn", "tilly.main:app", "--workers", "1", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000", "--timeout",  "600"]
