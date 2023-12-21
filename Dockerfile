FROM python:3.11.4-slim-bullseye
WORKDIR /usr/src/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc

# install dependencies
RUN pip install --upgrade pip
ENV PIP_ROOT_USER_ACTION=ignore

COPY ./requirements.txt .
RUN  pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

COPY . /usr/src/app/

ENTRYPOINT [ "gunicorn", "blog.wsgi"]