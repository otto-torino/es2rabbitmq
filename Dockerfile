FROM python:3.6.8

RUN mkdir -p /app
WORKDIR /app

COPY ./ .

RUN pip install --trusted-host pypi.python.org -r requirements.txt

ENTRYPOINT ["sh", "docker-entrypoint.sh"]
