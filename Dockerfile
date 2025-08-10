FROM astral/uv:python3.12-bookworm-slim
WORKDIR /usr/src/amarkov
COPY . .
RUN uv sync

CMD [ "uv", "run", "src/main.py" ]