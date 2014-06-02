#!/bin/bash
export __JAVA_HOME__= $JAVA_HOME

/opt/spark-0.9.1/sbin/start-master.sh

while [ 1 ];
do
	tail -f /opt/spark-0.9.1/logs/*.out
        sleep 1
done
