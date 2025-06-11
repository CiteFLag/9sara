FROM debian as build

RUN apt-get update -y
RUN apt-get install build-essential gcc-multilib -y
ADD chall.c /tmp/chall.c
ADD Makefile /tmp/Makefile
RUN cd /tmp/; make all

FROM debian

RUN dpkg --add-architecture i386
RUN apt-get update -y
RUN apt-get install libc6:i386 libncurses5:i386 libstdc++6:i386 -y
RUN apt-get install socat procps -y
COPY --from=build /tmp/chall /pwn/chall
COPY flag.txt /pwn/flag.txt
WORKDIR /pwn

EXPOSE 2030

ENTRYPOINT ["sh", "-c", "exec socat -s TCP-LISTEN:2030,reuseaddr,fork EXEC:/pwn/chall,stderr"]