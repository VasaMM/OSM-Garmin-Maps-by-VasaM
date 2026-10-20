FROM python:3.12-slim-bookworm
ENV DEBIAN_FRONTEND=noninteractive PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl unzip openjdk-17-jre-headless osmctools \
    && rm -rf /var/lib/apt/lists/*
COPY docker/requirements.txt /opt/requirements.txt
# pybind11-rdp has no Linux ARM64 wheel; compile it inside the image only.
RUN apt-get update && apt-get install -y --no-install-recommends g++ \
    && pip install --no-cache-dir -r /opt/requirements.txt \
    && apt-get purge -y --auto-remove g++ \
    && rm -rf /var/lib/apt/lists/*
ARG MKGMAP_VERSION=4924
ARG SPLITTER_VERSION=654
RUN mkdir -p /opt/vasam-tools \
    && curl -fL --retry 3 https://www.mkgmap.org.uk/download/mkgmap-r${MKGMAP_VERSION}.zip -o /tmp/mkgmap.zip \
    && curl -fL --retry 3 https://www.mkgmap.org.uk/download/splitter-r${SPLITTER_VERSION}.zip -o /tmp/splitter.zip \
    && unzip -q /tmp/mkgmap.zip -d /opt/vasam-tools \
    && unzip -q /tmp/splitter.zip -d /opt/vasam-tools \
    && rm /tmp/mkgmap.zip /tmp/splitter.zip
WORKDIR /workspace
ENTRYPOINT ["python", "docker/entrypoint.py"]
CMD ["--area", "CZ", "--code-page", "unicode", "--en", "--logging"]
