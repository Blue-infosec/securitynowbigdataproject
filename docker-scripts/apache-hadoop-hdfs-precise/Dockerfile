FROM ubuntu:saucy

RUN apt-get update;

RUN apt-get install software-properties-common -y

RUN add-apt-repository ppa:webupd8team/java -y

RUN apt-get update && apt-get -y upgrade

RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections

RUN apt-get -y install oracle-java7-installer && apt-get clean

RUN update-alternatives --display java

ADD http://mirror.sdunix.com/apache/hadoop/common/hadoop-1.2.1/hadoop_1.2.1-1_x86_64.deb /root/

RUN dpkg -i /root/hadoop_1.2.1-1_x86_64.deb && rm /root/hadoop_1.2.1-1_x86_64.deb

RUN sed -i s/"files dns"/"dns files"/ /etc/nsswitch.conf

ADD files /root/hadoop_files

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle

VOLUME ["/data"]