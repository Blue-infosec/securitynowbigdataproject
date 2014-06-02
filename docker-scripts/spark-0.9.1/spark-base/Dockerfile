# Spark 0.9.1
# Version 0.9.1
#
FROM apache-hadoop-hdfs-precise:1.2.1

ENV SPARK_VERSION 0.9.1
ENV SPARK_HOME /opt/spark
ENV PATH $SPARK_HOME:$PATH

RUN apt-get install python-dev less net-tools apt-utils vim-tiny sudo openssh-server libyaml-0-2 iputils-ping git gzip wget curl python-pip -y
RUN /usr/bin/yes | sudo pip install nltk numpy

# Install Scala
ADD files/scala-2.11.1.deb /opt/scala-2.11.1.deb
RUN ls /opt -alh
RUN dpkg -i /opt/scala-2.11.1.deb

# Install Spark
ADD files/spark-0.9.1-bin-hadoop2.tgz /opt

RUN ls /opt -alh

RUN mv /opt/spark-0.9.1-bin-hadoop2 /opt/spark-0.9.1

# Add Shark config files and configure script
ADD files /root/spark_files

RUN cd /opt/spark-0.9.1; /opt/spark-0.9.1/sbt/sbt clean assembly

RUN echo "Set up and ready to run"
RUN ls -alh /opt