FROM ghcr.io/astral-sh/uv:0.10 AS uv

FROM python:3.14-slim AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=from=uv,source=/uv,target=/bin/uv \
	--mount=type=cache,target=/root/.cache/uv \
	uv export --frozen --no-emit-workspace --no-dev --no-editable -o requirements.txt && \
	python -m venv /opt/venv && \
	/opt/venv/bin/pip install -r requirements.txt

FROM python:3.14-slim

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY --from=builder /opt/venv /opt/venv
COPY ./src ./src

CMD ["python", "-m", "src.main"]
