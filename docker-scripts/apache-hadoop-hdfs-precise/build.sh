#!/bin/bash

rm -f files/files.hash
for i in `find . -type f | sed s/"\.\/"//`; do git hash-object $i | tr -d '\n'; echo -e "\t$i"; done > /tmp/files.hash
mv /tmp/files.hash files/files.hash
sudo docker build --no-cache -t apache-hadoop-hdfs-precise:1.2.1 .