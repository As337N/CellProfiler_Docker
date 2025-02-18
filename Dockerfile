FROM python:3.8-bullseye

RUN apt-get update && apt-get install -y \
    openjdk-11-jdk-headless \
    build-essential \
    libgtk-3-dev \
    && rm -rf /var/lib/apt/lists/*

ENV JAVA_HOME /usr/lib/jvm/java-11-openjdk-amd64

RUN pip install --upgrade pip setuptools wheel numpy
RUN pip install --verbose cellprofiler optuna pandas


