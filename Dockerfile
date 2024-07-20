FROM ubuntu:latest
LABEL authors="A"

ENTRYPOINT ["top", "-b"]