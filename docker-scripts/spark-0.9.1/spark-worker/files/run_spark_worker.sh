#!/bin/bash
. /opt/spark-0.9.1/conf/spark-env.sh
/opt/spark-0.9.1/bin/spark-class org.apache.spark.deploy.worker.Worker $MASTER
