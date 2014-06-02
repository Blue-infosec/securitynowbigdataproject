#master
FROM ubuntu:trusty

RUN apt-get install software-properties-common build-essential scala git  -y

RUN add-apt-repository ppa:webupd8team/java -y

RUN apt-get update && apt-get -y upgrade

RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections

ADD http://d3kbcqa49mib13.cloudfront.net/spark-1.0.0-bin-hadoop2.tgz /opt
RUN mv /opt/spark-1.0.0-bin-hadoop2 /opt/spark



FROM