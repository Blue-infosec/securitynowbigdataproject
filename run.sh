#!/bin/bash

git clone https://github.com/levidehaan/twAppDemo.git

./twAppDemo/docker-scripts/deploy/deploy.sh -i shark:0.9.0 -w 3 -v

