# Spark
FROM spark-base:0.9.0
MAINTAINER amplab amp-docker@eecs.berkeley.edu

# Expose TCP ports 7077 8080
EXPOSE 7077 8080

ADD files /root/spark_master_files

RUN (cd /opt/spark-0.9.0 && sbt/sbt clean compile)

CMD ["/root/spark_master_files/default_cmd"]
