FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
COPY run.sh .
RUN chmod +x run.sh
COPY docker-compose.yml .
COPY src/ src/

RUN pip install --no-cache-dir .

EXPOSE 8000

ENV APP_MODE=server

CMD ["./run.sh"]