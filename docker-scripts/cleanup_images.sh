#!/bin/bash

function cleanImages(){
#remove the docker images
sudo docker images | grep "shark" | awk '{print $3}' | xargs sudo docker rmi
sudo docker images | grep "spark" | awk '{print $3}' | xargs sudo docker rmi
sudo docker images | grep "dnsmasq" | awk '{print $3}' | xargs sudo docker rmi
sudo docker images | grep "apache-hadoop" | awk '{print $3}' | xargs sudo docker rmi
sudo docker images | grep "<none>" | awk '{print $3}' | xargs sudo docker rmi

}

function cleanContainers(){
#remove the docker containers
sudo docker ps -a | grep "spark" | awk '{print $1}' | xargs sudo docker rm
sudo docker ps -a | grep "shark" | awk '{print $1}' | xargs sudo docker rm
sudo docker ps -a | grep "dnsmasq" | awk '{print $1}' | xargs sudo docker rm
sudo docker ps -a | grep "apache-hadoop" | awk '{print $1}' | xargs sudo docker rm
sudo docker ps -a | grep "sbt/sbt" | awk '{print $1}' | xargs sudo docker rm
sudo docker ps -a | grep "/opt/spa" | awk '{print $1}' | xargs sudo docker rm
sudo docker ps -a | grep "cd /opt" | awk '{print $1}' | xargs sudo docker rm

}

cleanImages

cleanContainers

cleanImages