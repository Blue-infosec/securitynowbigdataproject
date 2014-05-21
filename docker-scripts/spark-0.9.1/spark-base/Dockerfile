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

# Install Scala
ADD http://www.scala-lang.org/files/archive/scala-$SCALA_VERSION.tgz /
RUN (cd / && gunzip < scala-$SCALA_VERSION.tgz)|(cd /opt && tar -xvf -)
RUN rm /scala-$SCALA_VERSION.tgz

# Install Spark
ADD http://mirror.nexcess.net/apache/incubator/spark/spark-$SPARK_VERSION/spark-$SPARK_VERSION-bin-hadoop2.tgz /
RUN (cd / && gunzip < spark-$SPARK_VERSION-bin-hadoop2.tgz)|(cd /opt && tar -xvf -)
RUN (ln -s /opt/spark-$SPARK_VERSION-bin-hadoop2 /opt/spark-$SPARK_VERSION && rm /spark-$SPARK_VERSION-bin-hadoop2.tgz)

# Add Shark config files and configure script
ADD files /root/spark_files

#WORKDIR /opt/spark-$SPARK_VERSION
#RUN (sbt/sbt clean compile && sbt/sbt assembly)