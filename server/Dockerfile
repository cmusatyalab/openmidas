FROM nvidia/cuda:11.5.1-cudnn8-devel-ubuntu18.04
LABEL maintainer="Satyalab, satya-group@lists.andrew.cmu.edu"

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    PATH="/openmidas-server/.venv/bin:$PATH"

RUN apt-get update && apt-get install -y \
    git \
    libgl1 \
    python3.8 \
    python3.8-venv \
    python3-pip \
    wget \
 && apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN --mount=type=cache,target=/root/.cache \
    python3.8 -m pip install --upgrade pip keyrings.alt \
 && python3.8 -m pip install poetry

# You can speed up build slightly by reducing build context with
#     git archive --format=tgz HEAD | docker build -t openscout -
WORKDIR /openmidas-server

# install dependencies
COPY poetry.lock pyproject.toml /openmidas-server/
RUN --mount=type=cache,target=/root/.cache \
    poetry install --no-cache --only main --no-root
#RUN poetry install --no-cache --only main --no-root \
# && rm -rf /root/.cache/pypoetry

COPY . /openmidas-server/

RUN --mount=type=cache,target=/root/.cache \
    poetry install --only main

EXPOSE 5555 9099
ENTRYPOINT ["./entrypoint.sh"]
