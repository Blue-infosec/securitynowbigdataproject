FROM ubuntu:14.04

RUN apt-get update; apt-get upgrade -y; apt-get install software-properties-common git python  -y

RUN add-apt-repository ppa:webupd8team/java -y

RUN apt-get update && apt-get -y upgrade

RUN echo oracle-java7-installer shared/accepted-oracle-license-v1-1 select true | /usr/bin/debconf-set-selections

RUN apt-get -y install oracle-java7-installer && apt-get clean

RUN update-alternatives --display java

ADD http://mirror.sdunix.com/apache/hadoop/common/hadoop-2.6.0/hadoop-2.6.0-src.tar.gz /root/hadoop-2.6.0-src.tar.gz

RUN tar -xvf -C /usr/local/ /root/hadoop-2.6.0-src.tar.gz && cd /usr/local && ln -s ./hadoop-2.6.0 hadoop

ENV HADOOP_PREFIX /usr/local/hadoop

RUN sed -i '/^export JAVA_HOME/ s:.*:export JAVA_HOME=/usr/java/default\nexport HADOOP_PREFIX=/usr/local/hadoop\nexport HADOOP_HOME=/usr/local/hadoop\n:' $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

RUN sed -i '/^export HADOOP_CONF_DIR/ s:.*:export HADOOP_CONF_DIR=/usr/local/hadoop/etc/hadoop/:' $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh

RUN mkdir $HADOOP_PREFIX/input

RUN cp $HADOOP_PREFIX/etc/hadoop/*.xml $HADOOP_PREFIX/input

ADD core-site.xml.template $HADOOP_PREFIX/etc/hadoop/core-site.xml.template

RUN sed s/HOSTNAME/localhost/ /usr/local/hadoop/etc/hadoop/core-site.xml.template > /usr/local/hadoop/etc/hadoop/core-site.xml

ADD hdfs-site.xml $HADOOP_PREFIX/etc/hadoop/hdfs-site.xml

ADD mapred-site.xml $HADOOP_PREFIX/etc/hadoop/mapred-site.xml

ADD yarn-site.xml $HADOOP_PREFIX/etc/hadoop/yarn-site.xml

RUN $HADOOP_PREFIX/bin/hdfs namenode -format

ADD ssh_config /root/.ssh/config

RUN rm /usr/local/hadoop/lib/native/* && curl -Ls http://dl.bintray.com/sequenceiq/sequenceiq-bin/hadoop-native-64-2.6.0.tar|tar -x -C /usr/local/hadoop/lib/native/ && chmod 600 /root/.ssh/config && chown root:root /root/.ssh/config

RUN yum install -y python-setuptools && easy_install pip && curl https://bitbucket.org/pypa/setuptools/raw/bootstrap/ez_setup.py -o - | python && pip install supervisor
ADD supervisord.conf /etc/supervisord.conf

ADD bootstrap.sh /etc/bootstrap.sh
RUN chown root:root /etc/bootstrap.sh
RUN chmod 700 /etc/bootstrap.sh

ENV BOOTSTRAP /etc/bootstrap.sh

# workingaround docker.io build error
RUN ls -la /usr/local/hadoop/etc/hadoop/*-env.sh
RUN chmod +x /usr/local/hadoop/etc/hadoop/*-env.sh
RUN ls -la /usr/local/hadoop/etc/hadoop/*-env.sh

# fix the 254 error code
RUN sed  -i "/^[^#]*UsePAM/ s/.*/#&/"  /etc/ssh/sshd_config
RUN echo "UsePAM no" >> /etc/ssh/sshd_config
RUN echo "Port 2122" >> /etc/ssh/sshd_config


RUN service ssh start && $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh && $HADOOP_PREFIX/sbin/start-dfs.sh && $HADOOP_PREFIX/bin/hdfs dfs -mkdir -p /user/root
RUN service ssh start && $HADOOP_PREFIX/etc/hadoop/hadoop-env.sh && $HADOOP_PREFIX/sbin/start-dfs.sh && $HADOOP_PREFIX/bin/hdfs dfs -put $HADOOP_PREFIX/etc/hadoop/ input

RUN sed -i s/"files dns"/"dns files"/ /etc/nsswitch.conf

RUN git clone git://github.com/apache/spark.git -b branch-1.2

RUN MAVEN_OPTS="-Xmx2g -XX:MaxPermSize=512M -XX:ReservedCodeCacheSize=512m" mvn -Pyarn -Phadoop-2.4 -Dhadoop.version=VERSION -DskipTests clean package

ADD files /root/hadoop_files

ENV JAVA_HOME /usr/lib/jvm/java-7-oracle

VOLUME ["/data"]

CMD ["/etc/bootstrap.sh", "-d"]

EXPOSE 50020 50090 50070 50010 50075 8031 8032 8033 8040 8042 49707 22 8088 8030
