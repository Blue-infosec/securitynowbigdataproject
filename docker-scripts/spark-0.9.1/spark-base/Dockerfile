# Spark 0.9.1
# Version 0.9.1
#
FROM apache-hadoop-hdfs-precise:1.2.1

MAINTAINER amplab amp-docker@eecs.berkeley.edu

ENV SCALA_VERSION 2.11.0
ENV SPARK_VERSION 0.9.1
ENV SCALA_HOME /opt/scala-$SCALA_VERSION
ENV SPARK_HOME /opt/spark-$SPARK_VERSION
ENV PATH $SPARK_HOME:$SCALA_HOME/bin:$PATH

RUN apt-get install python-dev less net-tools apt-utils vim-tiny sudo openssh-server libyaml-0-2 iputils-ping git wget curl python-pip -y
RUN /usr/bin/yes | sudo pip install nltk numpy

# Install Scala
ADD http://www.scala-lang.org/files/archive/scala-$SCALA_VERSION.tgz /
RUN (cd / && gunzip < scala-$SCALA_VERSION.tgz)|(cd /opt && tar -xvf -)
RUN rm /scala-$SCALA_VERSION.tgz

WORKDIR /opt/scala-2.11.0/ RUN export PATH=`pwd`/bin:$PATH && export SCALA_HOME=`pwd`

# Install Spark
ADD http://d3kbcqa49mib13.cloudfront.net/spark-0.9.1-bin-hadoop2.tgz /opt

WORKDIR /opt RUN tar -xvf spark-0.9.1-bin-hadoop2.tgz
WORKDIR /opt RUN (ln -s /opt/spark-0.9.1-bin-hadoop2 /opt/spark-0.9.1 && rm spark-0.9.1-bin-hadoop2.tgz)

# Add Shark config files and configure script
ADD files /root/spark_files

WORKDIR /opt/spark-0.9.1 RUN sbt/sbt clean assembly