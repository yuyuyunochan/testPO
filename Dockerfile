# Берем официальный образ Jenkins
FROM jenkins/jenkins:lts-jdk11

USER root
RUN apt-get update && \
    apt-get install -y python3 python3-dev python3-pip && \
    rm -rf /var/lib/apt/lists/*
USER jenkins