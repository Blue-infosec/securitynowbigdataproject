#!/bin/bash

git clone https://github.com/levidehaan/twAppDemo.git

./twAppDemo/docker-scripts/deploy/deploy.sh -i shark:0.9.0 -w 3 -v

SHELL_ID=$(sudo docker run -i -t --name="twmongo" -p 27017:27017 -p 28017:28017 ehazlett/mongodb:latest)

  if [ "$SHELL_ID" = "" ]; then
        echo "error: could not start shell container from image $IMAGENAME"
        exit 1
    fi

SHELL_IP=$(docker inspect $SHELL_ID | grep IPAddress | awk '{print $2}' | tr -d '":,')

mongoimport --host $SHELL_IP:27017 --db securitynow --collection securitynow --type tsv --file "data_dir/SecurityNow453.tsv" --headerline

./docker-scripts/apache-hadoop-hdfs-precise/build.sh
