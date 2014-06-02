# Spark
FROM spark-base:0.9.1

ENV SPARK_WORKER_PORT 8888

EXPOSE 8888

ADD files /root/spark_shell_files

# Add the entrypoint script for the master
ENTRYPOINT ["/root/spark_shell_files/default_cmd"]
