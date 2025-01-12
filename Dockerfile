FROM python:3.11

RUN apt-get update && apt-get install -y python3-opencv

WORKDIR /usr/src
COPY src ./

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv
RUN uv venv
RUN uv pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["./entrypoint.sh"]
