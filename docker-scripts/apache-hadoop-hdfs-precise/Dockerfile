# Base Ubuntu Trusty 14.04 LTS image
FROM ubuntu:saucy

# Setup a volume for data
VOLUME ["/data"]

# Set correct source list
# RUN echo "deb http://archive.ubuntu.com/ubuntu saucy main universe" > /etc/apt/sources.list

RUN apt-get update; apt-get upgrade -y

RUN apt-get install -y less net-tools apt-utils vim-tiny sudo openssh-server iputils-ping software-properties-common git wget

RUN add-apt-repository ppa:webupd8team/java -y

RUN apt-get update && apt-get -y upgrade

RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections

RUN apt-get -y install oracle-java7-installer oracle-java6-installer && apt-get clean

# Install Hadoop
ADD http://mirror.sdunix.com/apache/hadoop/common/hadoop-1.2.1/hadoop_1.2.1-1_x86_64.deb /root/
RUN dpkg -i /root/hadoop_1.2.1-1_x86_64.deb && rm /root/hadoop_1.2.1-1_x86_64.deb

# Docker messes up /etc/hosts and adds two entries for 127.0.0.1
# we try to recover from that by giving /etc/resolv.conf and therefore
# the nameserver priority
RUN sed -i s/"files dns"/"dns files"/ /etc/nsswitch.conf

# add Hadoop config file templates
ADD files /root/hadoop_files

# Set JAVA_HOME
ENV JAVA_HOME /usr/lib/jvm/java-7-openjdk-amd64
