FROM ubuntu:latest
LABEL authors="ikrom"

ENTRYPOINT ["top", "-b"]