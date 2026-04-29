#!/bin/bash

docker load < my-app.tar
docker stop my-app || true
docker rm my-app || true
docker run -d -p 80:5000 --name my-app my-app
