FROM python:3.12-slim AS runtime
WORKDIR /app
COPY pyproject.toml README.md ./
COPY src ./src
COPY datasets ./datasets
COPY examples ./examples
RUN pip install --no-cache-dir .
USER 65532:65532
ENTRYPOINT ["inference-index"]

