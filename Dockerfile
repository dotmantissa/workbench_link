FROM python:3.14-slim@sha256:9aaa474097d094040649f2162a627c0049b408f52138d980916788d80f04802f
RUN apt-get update && apt-get install -y --no-install-recommends bash ripgrep coreutils git \
    && rm -rf /var/lib/apt/lists/*
COPY workbench_link/__init__.py workbench_link/runner.py workbench_link/protocol.py workbench_link/errors.py /opt/workbench_link/
ENV PYTHONPATH=/opt PYTHONDONTWRITEBYTECODE=1
WORKDIR /workspace
ENTRYPOINT ["python", "-u", "-m", "workbench_link.runner"]
