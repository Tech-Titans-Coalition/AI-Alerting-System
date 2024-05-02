FROM python:3.7

COPY requirements.txt /opt/program/requirements.txt

RUN apt-get -y update && apt-get install -y --no-install-recommends \
         wget \
         nginx \
         ca-certificates \
         openssh-server \
         zlib1g \
         linux-image-amd64 \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install --no-cache-dir -r /opt/program/requirements.txt

ENV PYTHONUNBUFFERED=TRUE
ENV PYTHONDONTWRITEBYTECODE=TRUE
ENV PATH="/opt/program:${PATH}"
ENV MODEL_PATH="/opt/ml/model"

COPY algorithm /opt/program
WORKDIR /opt/program