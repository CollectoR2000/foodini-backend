FROM python:3.10.4-slim-bullseye

ENV TZ=Europe/Amsterdam
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

COPY ./requirements.txt /requirements.txt
RUN pip install --no-cache -r /requirements.txt && \
    rm -rf /requirements.txt

ARG PROJECT_VERSION
ENV PROJECT_VERSION=$PROJECT_VERSION

COPY ./foodini/ /app/

COPY ./CHANGELOG.md /CHANGELOG.md

HEALTHCHECK --interval=30s --timeout=15s --retries=3 CMD [ "./healthcheck.py" ]

CMD [ "python3", "/app/foodini.py" ]
