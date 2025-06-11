FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    gcc \
    make \
    socat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY Makefile .
COPY chall.c .

COPY flag.txt .
RUN chmod 444 /app/flag.txt

RUN make

EXPOSE 28621

CMD socat TCP-LISTEN:28621,fork,reuseaddr EXEC:./super-saiyan,pty,stderr,sigint,sighup,setsid,raw,echo=0 