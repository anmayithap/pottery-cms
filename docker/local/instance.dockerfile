FROM python:3.12-alpine AS compiller

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV POETRY_VIRTUALENVS_CREATE=false
ENV PROJECT_DIR /opt/pottery
ENV VENV "${PROJECT_DIR}/venv"

WORKDIR ${PROJECT_DIR}

RUN apk add --no-cache --update \
    bash \
    && rm -rf ~/.cache/* /usr/local/share/man /tmp/* \
    && python3 -m venv ${VENV} \
    && pip install poetry \
    && exit 0

ENV PATH ${VENV}/bin:${PATH}

COPY pyproject.toml poetry.lock ${PROJECT_DIR}/

RUN poetry export --with=dev > requirements.txt \
    && pip install -Ur requirements.txt

FROM python:3.12-alpine AS runner

ENV PYTHONBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PROJECT_DIR /opt/pottery
ENV VENV "$PROJECT_DIR/venv"

WORKDIR ${PROJECT_DIR}

COPY --from=compiller ${VENV} ${VENV}

ENV PATH ${VENV}/bin:${PATH}

COPY ./ ${PROJECT_DIR}
